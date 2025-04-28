# A neural network implementation (almost the same as backpropagation.py,
# except for a tiny refactoring in the back() function).
import numpy as np
#import mnist

class model:
    def __init__(self, n_input_variables, n_hidden_nodes, n_classes):
        self.w1, self.w2 = self.initialize_weights(n_input_variables, n_hidden_nodes, n_classes)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))


    def softmax(self, logits):
        exponentials = np.exp(logits)
        return exponentials / np.sum(exponentials, axis=1).reshape(-1, 1)


    def sigmoid_gradient(self, sigmoid):
        return np.multiply(sigmoid, (1 - sigmoid))


    def loss(self, Y, y_hat):
        return -np.sum(Y * np.log(y_hat)) / Y.shape[0]


    def prepend_bias(self, X):
        return np.insert(X, 0, 1)


    def forward(self, X):
        h = self.sigmoid(np.matmul(self.prepend_bias(X), self.w1))
        y_hat = self.sigmoid(np.matmul(self.prepend_bias(h), self.w2))
        return (y_hat, h)


    def back(self, X, Y, y_hat, h):

        # think it is messing up mat mul over single axis
        w2_gradient = self.prepend_bias(h).reshape(-1, 1)@(y_hat - Y).reshape(1, -1) / X.shape[0]
        # w1_gradient = np.matmul(self.prepend_bias(X).T, np.matmul(y_hat - Y, self.w2[1:].T) * self.sigmoid_gradient(h)) / X.shape[0]
        w1_gradient = (self.prepend_bias(X).reshape(-1, 1) @ ((y_hat -Y).reshape(1, -1) @ self.w2[1:].T * self.sigmoid_gradient(h))) / X.shape[0]
        return (w1_gradient, w2_gradient)


    def classify(self, X):
        y_hat, _ = self.forward(X)
        labels = np.argmax(y_hat)
        return labels.reshape(-1, 1)
    
    def predict(self, X):
        y_hat, _ = self.forward(X)
        return y_hat


    def initialize_weights(self, n_input_variables, n_hidden_nodes, n_classes):
        w1_rows = n_input_variables + 1
        w1 = np.zeros((w1_rows, n_hidden_nodes))

        w2_rows = n_hidden_nodes + 1
        w2 = np.zeros((w2_rows, n_classes))

        return (w1, w2)
    
    def save_weights(self):
        np.save("w1.npy", self.w1)
        np.save("w2.npy", self.w2)
    
    def load_weights(self):
        self.w1 = np.load("w1.npy")
        self.w2 = np.load("w2.npy")


    def report(self, iteration, X_train, Y_train, X_test, Y_test):
        y_hat, _ = self.forward(X_train)
        training_loss = self.loss(Y_train, y_hat)
        classifications = self.classify(X_test)
        accuracy = np.average(classifications == Y_test) * 100.0
        print("Iteration: %5d, Loss: %.8f, Accuracy: %.2f%%" %
            (iteration, training_loss, accuracy))


    def train(self, X_train, Y_train, iterations, lr, X_test=None, Y_test=None):
        for iteration in range(iterations):
            y_hat, h = self.forward(X_train)
            w1_gradient, w2_gradient = self.back(X_train, Y_train, y_hat, h)
            self.w1 = self.w1 - (w1_gradient * lr)
            self.w2 = self.w2 - (w2_gradient * lr)
            if X_test is not None and Y_test is not None:
                self.report(iteration, X_train, Y_train, X_test, Y_test)


# this works but this is REALLY slow
# mod = model(n_input_variables=mnist.X_train.shape[1], n_hidden_nodes=200, n_classes=mnist.Y_train.shape[1])
# mod.train(mnist.X_train, mnist.Y_train, mnist.X_test, mnist.Y_test, iterations=275, lr=0.01)