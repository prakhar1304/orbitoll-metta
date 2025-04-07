(adam   10 1000  male )
(pokemon 1  20   femal)
(pika    2   4   male )
(uuo    4   6   femal)


(pokemon isPokemof adam)
(pokemon  isPokemof uuo)

; (adam isPokemof pokemon)
; (uuo  isPokemof pokemon)
(CG07AU599 (PRAKHAR MADHARIA) WALLET_ADDRESS VEHICAL_TYPE  RC_DETAIL)


; (= (isSibling $x $y)
;        (match &self ($n isPokemof $x) (match &self ($n isPokemof $y ) True))
       
; )

; !(isSibling adam uuo)

; !(match  &self ( CG07AU599 $x $y $z $p)  ( "OWNER_NAME:" , $x  , "WALLET_ADDRESS:" , $y , "VEHICAL_TYPE:" , $z , "RC_DETAIL:" , $p ))
; !(match  &self ( adam $x $y $z)  ("VEHICAL_NO:" , $x ))


;----------------
;place days  foodcostPerDay HotelCPerDay  (twoWheel Car Metro) best  season
(Delhi 4 200 500 (100 200 300 )  december) 
(mumbai 4 200 500 (100 200 300 )  december) 
(pune 4 200 500 (100 200 300 )  december) 

(tajmahal isTouristPlace Delhi )
(agra isTouristPlace Delhi)
(tu_jiyan_ha isTouristPlace mumbai)
(pokemon isTouristPlace mumbai)
((gate way of india) isTouristPlace mumbai)

(tajmahal hasLogLat  (27.1751 78.0421))
(agra hasLogLat (27.1767 78.0081))
(tu_jiyan_ha hasLogLat (27.1767 78.0081))
(pokemon hasLogLat (27.1767 78.0081))

; (=  (isloglat  $x)
;     (match &self ($n isTouristPlace $x)  $n )
; )
(=  (isloglat  $x)
    (match &self ($n isTouristPlace $x)  (match &self ($n  hasLogLat $p) ("touristplace" $n  "has logitue latitue" $p)) )
)
(=  (isdetail  $x)
    (match &self ($x  $y $z $p ($k  $u $d) $w)  ($x "no of days" $y "food cost perday " $z  "hotel cost  perday" $p  "bike car bus" $k $u $d "best time" $w )  )
)

; !(match  &self ( CG07AU599 $x $y $z $p)  ( "OWNER_NAME:" , $x  , "WALLET_ADDRESS:" , $y , "VEHICAL_TYPE:" , $z , "RC_DETAIL:" , $p ))
 !(match &self (Delhi  $y $z $p $k  $u $d $w)  $y  )

!(isloglat Delhi)
!(isdetail Delhi)

; ,$n  will  not   print