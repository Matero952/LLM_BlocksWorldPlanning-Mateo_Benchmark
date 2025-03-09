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

    TEST45 = 'pick: red_block\nplace: table'
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

    BADTEST1 = 'pick: red_block place: red_block'
    BADTEST2 = 'pick: blue_block place: blue_block'
    BADTEST3 = 'pick: yellow_block place: yellow_block'
#TODO Make algorithm file that automatically generates these based on the pddl domain and states.
