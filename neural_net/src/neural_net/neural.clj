(ns neural_net.neural
  (:require [incanter.core :as core])
  (:require [incanter.matrix :as matrix]))

(defrecord NeuralNet [num_layers sizes biases weights])


(defn dot [x y])


(defn sigmoid [z]
  (/ (1.0) (+ (1.0) (core/exp -z))))


(defn feedForward [net a]
  (def feeds (map #(def a (sigmoid (+ (reduce + (+ %1 a)) %2))) (:weights net) (:biases net))))


(defn stochGradDesc [net training_data num_sessions batch_size learning_rate test_data]
  (cond (test_data) (def test_length (count test_data)))
  (def train_length (count training_data))
  (def session_datas (repeatedly num_sessions (partial shuffle training_data)))
  (def session_batches (map #(partition batch_size batch_size nil %) session_datas))
  (for [batches session_batches] (do
                                  (map #(update_batch net batch learning_rate) batches)
                                  (cond (test_data)(evaluate net test_data)))))


(defn update_batch [net batch learning_rate]
  (def biases (matrix (count (first (:biases net))))
  (def gradients (map #(backprop net %) batch))
  (def))
