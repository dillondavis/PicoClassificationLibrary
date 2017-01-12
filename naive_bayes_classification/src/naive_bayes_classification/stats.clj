(ns naive_bayes_classification.stats
  (:require [clojure.java.io :as io]))

(defn accuracy
  [real_classes result_classes]
  (def num_right (count (for [i (range (count real_classes))
    :when (= (nth real_classes i) (nth result_classes i))] i)))
  (/ (float num_right) (count real_classes)))


(defn get_confusion_derivations
  [real_classes result_classes target_class]
  (def results (for [i (range (count real_classes))] [(nth real_classes i) (nth result_classes i)]))

  (def tpos (count (filter #(let [real (first %) result (second %)]
    (and (= real target_class) (= real result))) results)))
  (def fpos (count (filter #(let [real (first %) result (second %)]
    (and (= result target_class) (not= real result))) results)))
  (def tneg (count (filter #(let [real (first %) result (second %)]
    (and (not= real target_class) (= real result))) results)))
  (def fneg (count (filter #(let [real (first %) result (second %)]
    (and (not= result target_class) (not= real result))) results)))
  (def derivs [(float tpos) (float fpos) (float tneg) (float fneg)])

  (cond (contains? derivs 0) (map inc derivs)
        :else derivs))


(defn print_stats
  [stats target_class filename]
  (with-open [w (io/writer (str filename ".metrics") :append true)]
    (do
      (.write w (str "Target Class: " target_class "\n"))
      (.write w (str "\tSensitivity: " (first stats) "\n"))
      (.write w (str "\tSpecificity: " (second stats) "\n"))
      (.write w (str "\tPrecision: " (nth stats 2) "\n"))
      (.write w (str "\tRecall: " (nth stats 3) "\n"))
      (.write w (str "\tF-1 Score: " (nth stats 4) "\n"))
      (.write w (str "\tF-Half Score: " (nth stats 5) "\n"))
      (.write w (str "\tF-2 Score: " (nth stats 6) "\n\n")))))


(defn get_stats
  [real_classes result_classes target]
  (def derivs (get_confusion_derivations real_classes result_classes target))
  (def tpos (first derivs))
  (def fpos (second derivs))
  (def tneg (nth derivs 2))
  (def fneg (nth derivs 3))

  (def sensitivity (/ tpos (+ tpos fneg)))
  (def specificity (/ tneg (+ tneg fpos)))
  (def precision (/ tpos (+ tpos fpos)))
  (def recall sensitivity)
  (def f1 (/ (* 2 tpos) (+ (* 2 tpos) fpos fneg)))
  (def fhalf (/ (* 1.25 (* precision recall)) (+ (* 0.25 precision) recall)))
  (def f2 (/ (* 5 (* precision recall)) (+ (* 4 precision) recall)))

  (list sensitivity specificity precision recall f1 fhalf f2))


(defn get_confusion_matrix
  [real_classes result_classes classes]
  (def results (for [i (range (count real_classes))] [(nth real_classes i) (nth result_classes i)]))
  (dorun (for [i classes j classes]
    (do
      (printf "%d " (count (filter #(and (= (first %) i) (= (second %) j)) results)))
      (cond (= j (last classes)) (printf "\n"))))))


(defn get_all_stats
  [real_classes result_classes classes filename]
  (get_confusion_matrix real_classes result_classes classes)
  (def all_stats (map #(get_stats real_classes result_classes %) classes))
  (with-open [w (io/writer (str filename ".metrics"))]
    (do
      (.write w (str filename " Metrics" "\n\n"))
      (.write w (str "Accuracy: " (accuracy real_classes result_classes) "\n\n"))))
  (dorun (map #(print_stats %1 %2 filename) all_stats classes)))
