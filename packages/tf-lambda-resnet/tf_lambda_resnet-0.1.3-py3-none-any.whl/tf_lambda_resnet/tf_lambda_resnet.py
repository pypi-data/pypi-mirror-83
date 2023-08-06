import tensorflow as tf # type: ignore
from einops.layers.tensorflow import Rearrange # type: ignore
from tensorflow import einsum, nn
from tensorflow.keras import initializers # type: ignore
from tensorflow.keras.layers import BatchNormalization, Conv2D, Conv3D, Layer # type: ignore


# helpers functions
def exists(val):
    return val is not None


def default(val, d):
    return val if exists(val) else d


class LambdaLayer(Layer):
    def __init__(self, *, dim_k, n=None, r=None, heads=4, dim_out=None, dim_u=1):
        super(LambdaLayer, self).__init__()

        self.out_dim = dim_out
        self.u = dim_u  # intra-depth dimension
        self.heads = heads

        assert (
            dim_out % heads
        ) == 0, (
            "values dimension must be divisible by number of heads for multi-head query"
        )
        self.dim_v = dim_out // heads
        self.dim_k = dim_k
        self.heads = heads

        self.to_q = Conv2D(self.dim_k * heads, 1, use_bias=False)
        self.to_k = Conv2D(self.dim_k * dim_u, 1, use_bias=False)
        self.to_v = Conv2D(self.dim_v * dim_u, 1, use_bias=False)

        self.norm_q = BatchNormalization()
        self.norm_v = BatchNormalization()

        self.local_contexts = exists(r)
        if exists(r):
            assert (r % 2) == 1, "Receptive kernel size should be odd"
            self.pos_conv = Conv3D(dim_k, (1, r, r), padding="same")
        else:
            assert exists(n), "You must specify the total sequence length (h x w)"
            self.pos_emb = self.add_weight(
                name="pos_emb",
                shape=(n, n, dim_k, dim_u),
                initializer=initializers.random_normal,
                trainable=True,
            )

    def call(self, x, **kwargs):
        _, hh, ww, _, u, h = *x.get_shape().as_list(), self.u, self.heads

        q = self.to_q(x)
        k = self.to_k(x)
        v = self.to_v(x)

        q = self.norm_q(q)
        v = self.norm_v(v)

        q = Rearrange("b hh ww (h k) -> b h k (hh ww)", h=h)(q)
        k = Rearrange("b hh ww (u k) -> b u k (hh ww)", u=u)(k)
        v = Rearrange("b hh ww (u v) -> b u v (hh ww)", u=u)(v)

        k = nn.softmax(k)

        Lc = einsum("b u k m, b u v m -> b k v", k, v)
        Yc = einsum("b h k n, b k v -> b n h v", q, Lc)

        if self.local_contexts:
            v = Rearrange("b u v (hh ww) -> b v hh ww u", hh=hh, ww=ww)(v)
            Lp = self.pos_conv(v)
            Lp = Rearrange("b v h w k -> b v k (h w)")(Lp)
            Yp = einsum("b h k n, b v k n -> b n h v", q, Lp)
        else:
            Lp = einsum("n m k u, b u v m -> b n k v", self.pos_emb, v)
            Yp = einsum("b h k n, b n k v -> b n h v", q, Lp)

        Y = Yc + Yp
        out = Rearrange("b (hh ww) h v -> b hh ww (h v)", hh=hh, ww=ww)(Y)
        return out

    def compute_output_shape(self, input_shape):
        return (*input_shape[:2], self.out_dim)

    def get_config(self):
        config = {"output_dim": (*self.input_shape[:2], self.out_dim)}
        base_config = super(LambdaLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class BottleNeck(tf.keras.layers.Layer):
    def __init__(self, filter_num, stride=1):
        super(BottleNeck, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(
            filters=filter_num, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.bn1 = tf.keras.layers.BatchNormalization()

        self.conv2 = LambdaLayer(dim_out=filter_num, dim_k=16, r=15, heads=4, dim_u=1)
        self.pool = (
            tf.keras.layers.AveragePooling2D()
            if stride != 1
            else tf.keras.layers.Layer()
        )

        self.conv3 = tf.keras.layers.Conv2D(
            filters=filter_num * 4, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.bn3 = tf.keras.layers.BatchNormalization()

        self.downsample = tf.keras.Sequential()
        self.downsample.add(
            tf.keras.layers.Conv2D(
                filters=filter_num * 4, kernel_size=(1, 1), strides=stride
            )
        )
        self.downsample.add(tf.keras.layers.BatchNormalization())

    def call(self, inputs, training=None, **kwargs):
        residual = self.downsample(inputs)

        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = tf.nn.relu(x)

        x = self.conv2(x)
        x = self.pool(x)
        x = tf.nn.relu(x)

        x = self.conv3(x)
        x = self.bn3(x, training=training)

        output = tf.nn.relu(tf.keras.layers.add([residual, x]))
        return output


def make_bottleneck_layer(filter_num, blocks, stride=1):
    res_block = tf.keras.Sequential()
    res_block.add(BottleNeck(filter_num, stride=stride))

    for _ in range(1, blocks):
        res_block.add(BottleNeck(filter_num, stride=1))

    return res_block


class LambdaResNet(tf.keras.Model):
    def __init__(self, layer_params, NUM_CLASSES=1000):
        super(ResNetTypeII, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(
            filters=64, kernel_size=(7, 7), strides=2, padding="same"
        )
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.pool1 = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), strides=2, padding="same"
        )

        self.layer1 = make_bottleneck_layer(filter_num=64, blocks=layer_params[0])
        self.layer2 = make_bottleneck_layer(
            filter_num=128, blocks=layer_params[1], stride=2
        )
        self.layer3 = make_bottleneck_layer(
            filter_num=256, blocks=layer_params[2], stride=2
        )
        self.layer4 = make_bottleneck_layer(
            filter_num=512, blocks=layer_params[3], stride=2
        )

        self.avgpool = tf.keras.layers.GlobalAveragePooling2D()
        self.fc = tf.keras.layers.Dense(
            units=NUM_CLASSES, activation=tf.keras.activations.softmax
        )

    def call(self, inputs, training=None, mask=None):
        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = tf.nn.relu(x)
        x = self.pool1(x)

        x = self.layer1(x, training=training)
        x = self.layer2(x, training=training)
        x = self.layer3(x, training=training)
        x = self.layer4(x, training=training)

        x = self.avgpool(x)
        output = self.fc(x)
        return output


def LambdaResnet18(**kwargs):
    """Constructs ResNet-18 model"""
    return LambdaResNet(layer_params=[2, 2, 2, 2], **kwargs)


def LambdaResnet34(**kwargs):
    """Constructs ResNet-34 model"""
    return LambdaResNet(layer_params=[3, 4, 6, 3], **kwargs)


def LambdaResnet50(**kwargs):
    """Constructs ResNet-50 model"""
    return LambdaResNet(layer_params=[3, 4, 6, 3], **kwargs)


def LambdaResnet101(**kwargs):
    """Constructs ResNet-101 model"""
    return LambdaResNet(layer_params=[3, 4, 23, 3], **kwargs)


def LambdaResnet152(**kwargs):
    """Constructs ResNet-152 model"""
    return LambdaResNet(layer_params=[3, 8, 36, 3], **kwargs)
