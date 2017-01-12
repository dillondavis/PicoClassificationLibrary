(ns naive_bayes_classification.naive
  (:require [clojure.data.csv :as csv])
  (:require [clojure.java.io :as io])
  (:require [naive_bayes_classification.stats :as stats]))

(defn get_data [filename]
  (with-open [in-file (io/reader filename)]
    (doall
      (csv/read-csv in-file))))


(defn split_data
  [data ratio]
  (let [data (shuffle data)
        m (count data)
        t (* m ratio)]
    [(take t data) (drop t data)]))


(defn get_classes [data]
  (def class_index (- (count (first data)) 1))
  (into [] (set (for [tup data] (nth tup class_index)))))


(defn separate_by_class [training_data classes]
  (def class_index (- (count (first training_data)) 1))
  (for [class classes] (filter #(= class (nth % class_index)) training_data)))


(defn get_data_stats [training_data]
  (def attribute_averages (map #(/ % (count training_data))(reduce #(map + %1 %2) training_data)))
  (def variances (reduce #(map + %1 %2) (for [tup training_data] (map #(Math/pow (- %1 %2) 2) tup attribute_averages))))
  (def stdevs (map #(Math/sqrt %) variances))
  (list attribute_averages stdevs))


(defn gaussian_prob [x mean stdev]
  (def exponent (Math/exp (/ (* (Math/pow (- x mean) 2) -1) (* 2 (Math/pow stdev 2)))))
  (* (/ 1 (* (Math/sqrt (* 2 (Math/PI))) stdev))) exponent)


(defn get_class_probability [tup class_stats]
  (reduce * (map gaussian_prob tup (first class_stats) (second class_stats))))


(defn get_tup_class [tup stats_by_class classes]
  (def probs (map #(get_class_probability tup %) stats_by_class))
  (def max_prob (apply max probs))
  (def class_index (first (for [i (range (count probs)) :when (= (nth probs i) max_prob)] i)))
  (nth classes class_index))


(defn classify [filename]
  (def data (for [tup (get_data filename)] (map read-string tup)))
  (def classes (get_classes data))
  (def split_data_sets (split_data data 0.67))
  (def training_tuples (first split_data_sets))
  (def test_tuples (second split_data_sets))
  (def test_data (map #(drop-last 1 %) test_tuples))
  (def test_classes (map first (map #(take-last 1 %) test_tuples)))

  (def data_by_classes (separate_by_class training_tuples classes))
  (def stats_by_class (map get_data_stats data_by_classes))
  (def result_classes (map #(get_tup_class % stats_by_class classes) test_data))
  (println (stats/accuracy test_classes result_classes))
  (stats/get_all_stats test_classes result_classes classes filename))
