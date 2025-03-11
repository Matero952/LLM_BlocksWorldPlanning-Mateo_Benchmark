from enum import Enum
class TestCases(Enum):
    #A bunch of test cases for the ActionOperator and StateTracker systems.
    TEST1 = 'pick: red_block place: table'
    TEST2 = 'pick: red_block place: yellow_block'
    TEST3 = 'pick: red_block place: blue_block'

    TEST4 = 'pick: blue_block place: table'
    TEST5 = 'pick: blue_block place: red_block'
    TEST6 = 'pick: blue_block place: yellow_block'

    TEST7 = 'pick: yellow_block place: table'
    TEST8 = 'pick: yellow_block place: red_block'
    TEST9 = 'pick: yellow_block place: blue_block'

    TEST10 = 'pick: red_block, place: table'
    TEST11 = 'pick: red_block, place: yellow_block'
    TEST12 = 'pick: red_block, place: blue_block'

    TEST13 = 'pick: blue_block, place: table'
    TEST14 = 'pick: blue_block, place: red_block'
    TEST15 = 'pick: blue_block, place: yellow_block'

    TEST16 = 'pick: yellow_block, place: table'
    TEST17 = 'pick: yellow_block, place: red_block'
    TEST18 = 'pick: yellow_block, place: blue_block'

    TEST19 = 'pick: red_block -> place: table'
    TEST20 = 'pick: red_block -> place: yellow_block'
    TEST21 = 'pick: red_block -> place: blue_block'

    TEST22 = 'pick: blue_block -> place: table'
    TEST23 = 'pick: blue_block -> place: red_block'
    TEST24 = 'pick: blue_block -> place: yellow_block'

    TEST25 = 'pick: yellow_block -> place: table'
    TEST26 = 'pick: yellow_block -> place: red_block'
    TEST27 = 'pick: yellow_block -> place: blue_block'

    TEST28 = 'pick: red_block ; place: table'
    TEST29 = 'pick: red_block ;; place: yellow_block'
    TEST30 = 'pick: red_block ;;; place: blue_block'

    TEST31 = 'pick: blue_block ; place: table'
    TEST32 = 'pick: blue_block ;; place: red_block'
    TEST33 = 'pick: blue_block ;;; place: yellow_block'

    TEST34 = 'pick: yellow_block ; place: table'
    TEST35 = 'pick: yellow_block ;; place: red_block'
    TEST36 = 'pick: yellow_block ;;; place: blue_block'

    TEST37 = 'pick: red_block ;;; -> place: table'
    TEST38 = 'pick: red_block ;; -> place: yellow_block'
    TEST39 = 'pick: red_block ; -> place: blue_block'

    TEST40 = 'pick: blue_block ;;; -> place: table'
    TEST41 = 'pick: blue_block ;; -> place: red_block'
    TEST42 = 'pick: blue_block ; -> place: yellow_block'

    TEST43 = 'pick: yellow_block ;;; -> place: table'
    TEST44 = 'pick: yellow_block ;; -> place: red_block'
    TEST45 = 'pick: yellow_block ; -> place: blue_block'

    # TEST45 = 'pick: red_block\nplace: table'
    TEST46 = 'pick: red_block\nplace: yellow_block'
    TEST47 = 'pick: red_block\nplace: blue_block'

    TEST48 = 'pick: blue_block\nplace: table'
    TEST49 = 'pick: blue_block\nplace: red_block'
    TEST50 = 'pick: blue_block\nplace: yellow_block'

    TEST51 = 'pick: yellow_block\nplace: table'
    TEST52 = 'pick: yellow_block\nplace: red_block'
    TEST53 = 'pick: yellow_block\nplace: blue_block'

    TEST54 = 'pick: red_block\nplace: table'
    TEST55 = 'pick: red_block\nplace: yellow_block'
    TEST56 = 'pick: red_block\nplace: blue_block'

    TEST57 = 'pick: blue_block\nplace: table'
    TEST58 = 'pick: blue_block\nplace: red_block'
    TEST59 = 'pick: blue_block\nplace: yellow_block'

    TEST60 = 'pick: yellow_block\nplace: table'
    TEST61 = 'pick: yellow_block\nplace: red_block'
    TEST62 = 'pick: yellow_block\nplace: blue_block'

    TEST63 = 'pick: red_block\nplace: table'
    TEST64 = 'pick: red_block\nplace: yellow_block'
    TEST65 = 'pick: red_block\nplace: blue_block'

    TEST66 = 'pick: blue_block\nplace: table'
    TEST67 = 'pick: blue_block\nplace: red_block'
    TEST68 = 'pick: blue_block\nplace: yellow_block'

    TEST69 = 'pick: yellow_block\nplace: table'
    TEST70 = 'pick: yellow_block\nplace: red_block'
    TEST71 = 'pick: yellow_block\nplace: blue_block'

    TEST72 = 'pick: red_block\nplace: table'
    TEST73 = 'pick: red_block\nplace: yellow_block'
    TEST74 = 'pick: red_block\nplace: blue_block'

    TEST75 = 'pick: blue_block\nplace: table'
    TEST76 = 'pick: blue_block\nplace: red_block'
    TEST77 = 'pick: blue_block\nplace: yellow_block'

    TEST78 = 'pick: yellow_block\nplace: table'
    TEST79 = 'pick: yellow_block\nplace: red_block'
    TEST80 = 'pick: yellow_block\nplace: blue_block'

    #Testing different model outputs.
    TEST81 = 'pick: red place: table'
    TEST82 = 'pick: red place: yellow'
    TEST83 = 'pick: red place: blue'

    TEST84 = 'pick: blue place: table'
    TEST85 = 'pick: blue place: red'
    TEST86 = 'pick: blue place: yellow'

    TEST87 = 'pick: yellow place: table'
    TEST88 = 'pick: yellow place: red'
    TEST89 = 'pick: yellow place: blue'

    TEST90 = 'pick: red, place: table'
    TEST91 = 'pick: red, place: yellow'
    TEST92 = 'pick: red, place: blue'

    TEST93 = 'pick: blue, place: table'
    TEST94 = 'pick: blue, place: red'
    TEST95 = 'pick: blue, place: yellow'

    TEST96 = 'pick: yellow, place: table'
    TEST97 = 'pick: yellow, place: red'
    TEST98 = 'pick: yellow, place: blue'

    TEST99 = 'pick: red -> place: table'
    TEST100 = 'pick: red -> place: yellow'
    TEST101 = 'pick: red -> place: blue'

    TEST102 = 'pick: blue -> place: table'
    TEST103 = 'pick: blue -> place: red'
    TEST104 = 'pick: blue -> place: yellow'

    TEST105 = 'pick: yellow -> place: table'
    TEST106 = 'pick: yellow -> place: red'
    TEST107 = 'pick: yellow -> place: blue'

    TEST108 = 'pick: red ; place: table'
    TEST109 = 'pick: red ;; place: yellow'
    TEST110 = 'pick: red ;;; place: blue'

    TEST111 = 'pick: blue ; place: table'
    TEST112 = 'pick: blue ;; place: red'
    TEST113 = 'pick: blue ;;; place: yellow'

    TEST114 = 'pick: yellow ; place: table'
    TEST115 = 'pick: yellow ;; place: red'
    TEST116 = 'pick: yellow ;;; place: blue'

    TEST117 = 'pick: red ;;; -> place: table'
    TEST118 = 'pick: red ;; -> place: yellow'
    TEST119 = 'pick: red ; -> place: blue'

    TEST120 = 'pick: blue ;;; -> place: table'
    TEST121 = 'pick: blue ;; -> place: red'
    TEST122 = 'pick: blue ; -> place: yellow'

    TEST123 = 'pick: yellow ;;; -> place: table'
    TEST124 = 'pick: yellow ;; -> place: red'
    TEST125 = 'pick: yellow ; -> place: blue'

    TEST126 = 'pick: red\nplace: table'
    TEST127 = 'pick: red\nplace: yellow'
    TEST128 = 'pick: red\nplace: blue'

    TEST129 = 'pick: blue\nplace: table'
    TEST130 = 'pick: blue\nplace: red'
    TEST131 = 'pick: blue\nplace: yellow'

    TEST132 = 'pick: yellow\nplace: table'
    TEST133 = 'pick: yellow\nplace: red'
    TEST134 = 'pick: yellow\nplace: blue'

    TEST135 = 'pick: red\nplace: table'
    TEST136 = 'pick: red\nplace: yellow'
    TEST137 = 'pick: red\nplace: blue'

    TEST138 = 'pick: blue\nplace: table'
    TEST139 = 'pick: blue\nplace: red'
    TEST140 = 'pick: blue\nplace: yellow'

    TEST141 = 'pick: yellow\nplace: table'
    TEST142 = 'pick: yellow\nplace: red'
    TEST143 = 'pick: yellow\nplace: blue'

    TEST144 = 'pick: red\nplace: table'
    TEST145 = 'pick: red\nplace: yellow'
    TEST146 = 'pick: red\nplace: blue'

    TEST147 = 'pick: blue\nplace: table'
    TEST148 = 'pick: blue\nplace: red'
    TEST149 = 'pick: blue\nplace: yellow'

    TEST150 = 'pick: yellow\nplace: table'
    TEST151 = 'pick: yellow\nplace: red'
    TEST152 = 'pick: yellow\nplace: blue'

    TEST153 = 'pick: red\nplace: table'
    TEST154 = 'pick: red\nplace: yellow'
    TEST155 = 'pick: red\nplace: blue'

    TEST156 = 'pick: blue\nplace: table'
    TEST157 = 'pick: blue\nplace: red'
    TEST158 = 'pick: blue\nplace: yellow'

    TEST159 = 'pick: yellow\nplace: table'
    TEST160 = 'pick: yellow\nplace: red'
    TEST161 = 'pick: yellow\nplace: blue'
    #Now, here are model outputs that SHOULD NOT work.
    BADTEST1 = 'pick: red place: red'
    BADTEST2 = 'pick: blue place: blue'
    BADTEST3 = 'pick: yellow place: yellow'

    BADTEST4 = 'pick: red place: purple'
    BADTEST5 = 'pick: blue place: orange'
    BADTEST6 = 'pick: yellow place: green'

    BADTEST7 = 'pick: red place: pink'
    BADTEST8 = 'pick: blue place: gray'
    BADTEST9 = 'pick: yellow place: brown'

    BADTEST10 = 'pick: red place: black'
    BADTEST11 = 'pick: blue place: white'
    BADTEST12 = 'pick: yellow place: silver'

    BADTEST13 = 'pick: red place: red_block'
    BADTEST14 = 'pick: blue place: blue_block'
    BADTEST15 = 'pick: yellow place: yellow_block'

    BADTEST16 = 'pick: red_block place: purple'
    BADTEST17 = 'pick: blue_block place: orange'
    BADTEST18 = 'pick: yellow_block place: green'

    BADTEST19 = 'pick: red place: red_block'
    BADTEST20 = 'pick: blue place: blue_block'
    BADTEST21 = 'pick: yellow place: yellow_block'

    BADTEST22 = 'pick: purple place: red'
    BADTEST23 = 'pick: orange place: blue'
    BADTEST24 = 'pick: green place: yellow'

    BADTEST25 = 'pick: pink place: red'
    BADTEST26 = 'pick: gray place: blue'
    BADTEST27 = 'pick: brown place: yellow'

    BADTEST28 = 'grab: red move_to: red'
    BADTEST29 = 'grab: blue move_to: blue'
    BADTEST30 = 'grab: yellow move_to: yellow'

    BADTEST31 = 'grab: red move_to: purple'
    BADTEST32 = 'grab: blue move_to: orange'
    BADTEST33 = 'grab: yellow move_to: green'

    BADTEST34 = 'grab: red move_to: pink'
    BADTEST35 = 'grab: blue move_to: gray'
    BADTEST36 = 'grab: yellow move_to: brown'

    BADTEST37 = 'grab: red move_to: black'
    BADTEST38 = 'grab: blue move_to: white'
    BADTEST39 = 'grab: yellow move_to: silver'

    BADTEST40 = 'grab: red move_to: red_block'
    BADTEST41 = 'grab: blue move_to: blue_block'
    BADTEST42 = 'grab: yellow move_to: yellow_block'

    BADTEST43 = 'grab: red_block move_to: purple'
    BADTEST44 = 'grab: blue_block move_to: orange'
    BADTEST45 = 'grab: yellow_block move_to: green'

    BADTEST46 = 'grab: red move_to: red_block'
    BADTEST47 = 'grab: blue move_to: blue_block'
    BADTEST48 = 'grab: yellow move_to: yellow_block'

    BADTEST49 = 'grab: purple move_to: red'
    BADTEST50 = 'grab: orange move_to: blue'
    BADTEST51 = 'grab: green move_to: yellow'

    BADTEST52 = 'grab: pink move_to: red'
    BADTEST53 = 'grab: gray move_to: blue'
    BADTEST54 = 'grab: brown move_to: yellow'

    BADTEST55 = 'lift: red drop_at: red'
    BADTEST56 = 'lift: blue drop_at: blue'
    BADTEST57 = 'lift: yellow drop_at: yellow'

    BADTEST58 = 'lift: red drop_at: purple'
    BADTEST59 = 'lift: blue drop_at: orange'
    BADTEST60 = 'lift: yellow drop_at: green'

    BADTEST61 = 'lift: red drop_at: pink'
    BADTEST62 = 'lift: blue drop_at: gray'
    BADTEST63 = 'lift: yellow drop_at: brown'

    BADTEST64 = 'lift: red drop_at: black'
    BADTEST65 = 'lift: blue drop_at: white'
    BADTEST66 = 'lift: yellow drop_at: silver'

    BADTEST67 = 'lift: red drop_at: red_block'
    BADTEST68 = 'lift: blue drop_at: blue_block'
    BADTEST69 = 'lift: yellow drop_at: yellow_block'

    BADTEST70 = 'lift: red_block drop_at: purple'
    BADTEST71 = 'lift: blue_block drop_at: orange'
    BADTEST72 = 'lift: yellow_block drop_at: green'

    BADTEST73 = 'lift: red drop_at: red_block'
    BADTEST74 = 'lift: blue drop_at: blue_block'
    BADTEST75 = 'lift: yellow drop_at: yellow_block'
