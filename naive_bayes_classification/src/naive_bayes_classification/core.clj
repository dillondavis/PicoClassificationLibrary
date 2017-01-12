(ns naive-bayes-classification.core
  (:gen-class)
  (:require [naive_bayes_classification.naive :as naive]))

(defn -main
  [& args]
  (naive/classify (first args)))
