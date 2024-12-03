(require '[clojure.core.reducers :as r] '[clojure.string :as str])

(def text (slurp "data/example.txt"))

(defn parse [text] (map 
                     (fn [x] 
                       (let [items (str/split x #"\s+")] 
                         (map (fn [y] (Integer/parseInt (str/trim y))) items))) 
                     (str/split (str/trim text) #"\n")))
(def items (parse text))

(def list_1 (map (fn [x] (let [[a b] x] a)) items))
(def list_2 (map (fn [x] (let [[a b] x] b)) items))

(defn count-occurrences [values]
  (r/fold(r/monoid #(merge-with + %1 %2)
           (constantly {}))(fn [m [k cnt]] (assoc m k (+ cnt (get m k 0))))
    (r/map #(vector % 1) values)
    )
  )
(def counts (count-occurrences list_2))


(def score (apply + 
             (map (fn [x] (* x (get counts x 0))) list_1)))

(print score)




