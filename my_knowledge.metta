;;!(match  &self ( CG07AU599 $x $y $z $p)  ( "OWNER_NAME:" , $x  , "WALLET_ADDRESS:" , $y , "VEHICAL_TYPE:" , $z , "RC_DETAIL:" , $p ))
(CG07AU599 (PRAKHAR MADHARIA) 0xABC123DEF456 car RC123456789)





(CG07AU510 (simon) 0xABC123DEF456 car RC123456789)
(cg (pk) 0x5da2Cb6EC30080bdE83857f67D541b20AaBe69CD Car lshlfh)


(= (vehicalDetail $x)
   (match &self ($n ($x) $y $z $p) ("vehical_no" $n "owner name" $x  "wallet address" $y  "vehical_type" $z "rc detail" $p)   )
)

!(vehicalDetail CG07AU599)