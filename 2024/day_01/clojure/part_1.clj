(require '[clojure.string :as str])

(def text (slurp "data/data.txt"))

(defn parse [text] (map (fn [x] 
            (let [items (str/split x #"\s+")] 
              (map 
                (fn [y] (Integer/parseInt (str/trim y))) items)
              )) 
            (str/split (str/trim text) #"\n")))
(def items (parse text))

(def list_1 (map (fn [x] (let [[a b] x] a)) items))
(def list_2 (map (fn [x] (let [[a b] x] b)) items))
(def ordered_items (map (fn [x y] [x y]) (sort list_1) (sort list_2)))

(def total (apply +
             (map (fn [z] (let [[x y] z] (abs (- x y)))) ordered_items))
            
            )
(print total)





