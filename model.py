import tensorflow as tf

# hyperparameters # hadie
WORD_DICT_SIZE = 13000  # hadie
LIMIT_SIZE = True  # hadie
EXAMPLE_NUMBER = 5  # will only work if LIMIT_SIZE is True # hadie
MY_EMBEDDING_DIM = 256  # hadie
UNIT_COUNT = 512  # hadie
MY_OPTIMIZER = tf.keras.optimizers.Adam()
MY_LOSS_OBJECT = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True, reduction='none')
EPOCH_COUNT = 10
REMOVE_CHECKPOINTS_AND_MODEL_AND_RETRAIN = True
DATASET = "mscoco"  # "mscoco" or "flickr8k" or "flickr30k"
TEST_SET_PROPORTION = 0.2
feature_extraction_model = "xception"  # hadie
split = 0.2  # 0 for training, 1 for testing => testing/training


class BahdanauAttention(tf.keras.Model): 

  def __init__(self, units):
    super(BahdanauAttention, self).__init__()
    self.W1 = tf.keras.layers.Dense(units)
    self.W2 = tf.keras.layers.Dense(units)
    self.V = tf.keras.layers.Dense(1)

  def call(self, features, hidden):
    # features(CNN_encoder output) shape == (batch_size, 64, embedding_dim)
    # hidden shape == (batch_size, hidden_size)
    # hidden_with_time_axis shape == (batch_size, 1, hidden_size)

    # print('ATTENTION')
    # print('input feature',features.shape)
    # print('input hidden shape', hidden.shape)

    hidden_with_time_axis = tf.expand_dims(hidden, 1)    
    # print('hidden_with_time_axis', hidden_with_time_axis.shape)

    # score shape == (batch_size, 64, hidden_size)
    score = tf.nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis))
    # print('score shape', score.shape)
    # print('score', score)

    # # hong test
    # A = self.W1(features)
    # print('A', A.shape)
    # B = self.W2(hidden_with_time_axis)
    # print('B', B.shape)
    # C = A + B
    # print('C', C.shape)
    # score = tf.nn.tanh(C)
    # print('score', score.shape)
    # # end hong test

    # attention_weights shape == (batch_size, 64, 1)
    # you get 1 at the last axis because you are applying score to self.V
    attention_weights = tf.nn.softmax(self.V(score), axis=1)
    # print('attention_weights shape', attention_weights.shape)

    # context_vector shape after sum == (batch_size, hidden_size)
    context_vector = attention_weights * features
    # print('context_vector shape 1', context_vector.shape)

    context_vector = tf.reduce_sum(context_vector, axis=1)
    # print('context_vector (output2) shape 2', context_vector.shape)

    return context_vector, attention_weights


class CNN_Encoder(tf.keras.Model):

    # Since you have already extracted the features and dumped it using pickle
    # This encoder passes those features through a Fully connected layer
    def __init__(self, embedding_dim):
        super(CNN_Encoder, self).__init__()
        # shape after fc == (batch_size, 64, embedding_dim)
        self.fc = tf.keras.layers.Dense(embedding_dim)

    def call(self, x):
        # print('ENCODER')
        # print('encoder input x', x.shape)

        x = self.fc(x)
        # print('x_fc shape', x.shape)

        x = tf.nn.relu(x)
        # print('x_relu shape', x.shape)

        return x

    def params_num(self):
        return self.count_params()


class RNN_Decoder(tf.keras.Model):

    def __init__(self, embedding_dim, units, vocab_size):
        super(RNN_Decoder, self).__init__()
        self.units = units

        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.lstm = tf.keras.layers.LSTM(self.units,
                                    return_sequences=True,
                                    return_state=True,
                                    recurrent_initializer='glorot_uniform')
        self.fc1 = tf.keras.layers.Dense(self.units)
        self.fc2 = tf.keras.layers.Dense(vocab_size)

        self.attention = BahdanauAttention(self.units)

    def call(self, x, features, hidden):
        # defining attention as a separate model

        # print('DECODER')
        # print('input x shape', x.shape)
        # print('features shape', features.shape)
        # print('hidden shape', hidden.shape)

        context_vector, attention_weights = self.attention(features, hidden)

        # x shape after passing through embedding == (batch_size, 1, embedding_dim)
        x = self.embedding(x)
        # print('x_embedding', x.shape)

        # x shape after concatenation == (batch_size, 1, embedding_dim + hidden_size)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        # print('x_concat', x.shape)

        # passing the concatenated vector to the LSTM
        output, state, _ = self.lstm(x)
        # print('output', output.shape)
        # print('state', state.shape)

        # shape == (batch_size, max_length, hidden_size)
        x = self.fc1(output)
        # print('x_fc1', x.shape)

        # x shape == (batch_size * max_length, hidden_size)
        x = tf.reshape(x, (-1, x.shape[2]))
        # print('x_reshape', x.shape)

        # output shape == (batch_size * max_length, vocab)
        x = self.fc2(x)
        # print('x_fc2', x.shape)

        return x, state, attention_weights

    def reset_state(self, batch_size):
        return tf.zeros((batch_size, self.units))

    def params_num(self):
        return self.count_params()


