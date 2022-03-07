// var DATA = {"a" : "b", "c" : "d"};

var Instructions_Dic = new Array();
var Connections_Dic = new Array();

//定义一个字典 存储边对应的 提示操作语句
// path_instruction_dic0 中的0 代表是 placeid=0的提示语
// path_instruction_dic0 中的1 代表是 placeid=1的提示语
//var path_instruction_dic0 = new Array(); 
//path_instruction_dic0['A_B'] = 'Go straight along the aisle and turn left at the corner.'
//path_instruction_dic0['B_C'] = 'Go straight along the aisle until you reach the glass aisle.'
//path_instruction_dic0['C_D'] = 'Take the stairs down to the next floor.'
//path_instruction_dic0['C_B'] = 'Go straight along the aisle and turn right when you reach the corner.'
//path_instruction_dic0['B_A'] = 'Keep walking until you see the rest table.'
//path_instruction_dic0['D_C'] = 'Take the stairs upstairs to the upper floor.'


//var path_instruction_dic1 = new Array(); 
//path_instruction_dic1['A_B'] = 'Go straight along the aisle and turn left at the corner.'
//path_instruction_dic1['B_C'] = 'Go straight along the aisle until you reach the glass aisle.'
//path_instruction_dic1['C_D'] = 'Take the stairs down to the next floor.'
//path_instruction_dic1['C_B'] = 'Go straight along the aisle and turn right when you reach the corner.'
//path_instruction_dic1['B_A'] = 'Keep walking until you see the rest table.'
//path_instruction_dic1['D_C'] = 'Take the stairs upstairs to the upper floor.'

var path_instruction_dic0 = new Array(); 
path_instruction_dic0['Entrance1_StudentServices'] = 'Entrance1_Student Services.'
path_instruction_dic0['Entrance1_ChangingRoom1'] = 'Entrance1_Changing Room1.'
path_instruction_dic0['Entrance1_FirstFloor1'] = 'Entrance1_First Floor1.'
path_instruction_dic0['StudentServices_Entrance1'] = 'Student Services_Entrance1.'
path_instruction_dic0['StudentServices_MedicalSuites'] = 'Student Services_Medical Suites.'
path_instruction_dic0['StudentServices_ChangingRoom1'] = 'Student Services_Changing Room1.'
path_instruction_dic0['ChangingRoom1_StudentServices'] = 'Changing Room1_Student Services.'
path_instruction_dic0['ChangingRoom1_FemaleWC'] = 'Changing Room1_Female WC.'
path_instruction_dic0['ChangingRoom1_StudentsUnion'] = 'Changing Room1_Students Union(F106).'
path_instruction_dic0['ChangingRoom2_FemaleWC'] = 'Changing Room2_Female WC.'
path_instruction_dic0['ChangingRoom2_SportHall'] = 'Changing Room2_Sport Hall(F150).'
path_instruction_dic0['FemaleWC_ChangingRoom1'] = 'Female WC_Changing Room1'
path_instruction_dic0['FemaleWC_ChangingRoom2'] = 'Female WC_Changing Room2.'
path_instruction_dic0['FemaleWC_StudentsUnion'] = 'Female WC_Students Union(F106).'
path_instruction_dic0['StudentsUnion_ChangingRoom1'] = 'Students Union(F106)_Changing Room1.'
path_instruction_dic0['StudentsUnion_MaleWC'] = 'Students Union(F106)_Male WC.'
path_instruction_dic0['StudentsUnion_FemaleWC'] = 'Students Union(F106)_Female Wc.'
path_instruction_dic0['StudentsUnion_CarreersOffice'] = 'Students Union(F106)_Carreers Office.'
path_instruction_dic0['MaleWC_StudentsUnion'] = 'Male WC_Students Union(F106).'
path_instruction_dic0['MaleWC_ChangingRoom3'] = 'Male WC_Changing Room3.'
path_instruction_dic0['ChangingRoom3_MaleWC'] = 'Changing Room3_Male WC.'
path_instruction_dic0['ChangingRoom3_SportsHall'] = 'Changing Room3_Sports Hall(F150).'
path_instruction_dic0['SportsHall_ChangingRoom2'] = 'Sports Hall(F150)_Changing Room2.'
path_instruction_dic0['SportsHall_ChangingRoom3'] = 'Sports Hall(F150)_Changing Room3.'
path_instruction_dic0['SportsHall_SportsOffice'] = 'Sports Hall(F150)_Sports Office.'
path_instruction_dic0['SportsOffice_SportsHall'] = 'Sports Office_Sports Hall(F150).'
path_instruction_dic0['SportsOffice_Entrance2SportsOffice_Entrance2'] = 'Sports Office_Entrance2.'
path_instruction_dic0['Entrance2_SportsOffice'] = 'Entrance2_Sports Office.'
path_instruction_dic0['Entrance2_CareersOffice'] = 'Entrance2_Careers Office.'
path_instruction_dic0['Entrance2_Chaplin'] = 'Entrance2_Chaplin.'
path_instruction_dic0['Entrance2_FirstFloor2'] = 'Entrance2_First Floor2.'
path_instruction_dic0['Chaplin_Entrance2'] = 'Chaplin_Entrance2.'
path_instruction_dic0['Chaplin_CareersOffice'] = 'Chaplin_Careers Office.'
path_instruction_dic0['CareersOffice_StudentsUnion'] = 'Careers Office_Students Union(F106).'
path_instruction_dic0['CareersOffice_Chaplin'] = 'Careers Office_Chaplin.'
path_instruction_dic0['CareersOffice_Entrance2'] = 'Careers Office_Entrance2.'
path_instruction_dic0['MedicalSuites_StudentServices'] = 'Medical Suites_Student Services.'
path_instruction_dic0['FirstFloor1_Entrance1'] = 'First Floor1_Entrance1.'
path_instruction_dic0['FirstFloor2_Entrance2'] = 'First Floor2_Entrance2.'


// var connection0 = [
//            ['A', [['B', 20], ['D', 150]] ], 
//            ['B', [['A', 20], ['C', 40]] ], 
//            ['C', [['B', 40], ['D', 20]] ], 
//            ['D', [['A', 150],['C', 20]] ]
//        ];


//var connection1 = [
//            ['A', [['B', 20]] ], 
//            ['B', [['A', 20]] ], 
//            ['C', [['D', 10] ] ], 
//            ['D', [['C', 10] ]]
//       ];
        


var connection0 = [
            ['Entrance1', [['StudentServices', 5], ['ChangingRoom1', 20], ['FirstFloor1',30]] ], 
            ['StudentServices', [['Entrance1', 5], ['MedicalSuites', 20], ['ChangingRoom1', 15]] ], 
            ['ChangingRoom1', [['StudentServices', 15], ['FemaleWC', 20], ['StudentsUnion', 15]] ], 
            ['ChangingRoom2', [['FemaleWC', 5],['SportHall', 8]] ],
            ['FemaleWC', [['ChangingRoom1', 20], ['ChangingRoom2', 5], ['StudentsUnion', 10]] ],
            ['StudentsUnion', [['ChangingRoom1', 15], ['MaleWC', 10], ['FemaleWC', 10], ['CarreersOffice', 15]] ],
            ['MaleWC', [['StudentsUnion', 10], ['ChangingRoom3', 5]] ],
            ['ChangingRoom3', [['MaleWC', 5], ['SportsHall', 5]] ],
            ['SportsHall', [['ChangingRoom2', 8], ['ChangingRoom3', 5], ['SportsOffice', 10]] ],
            ['SportsOffice', [['SportsHall(F150)', 10], ['Entrance2', 15]] ],
            ['Entrance2', [['SportsOffice', 15], ['CareersOffice', 10], ['Chaplin', 20], ['FirstFloor2', 30]] ],
            ['Chaplin', [['Entrance2', 20], ['CareersOffice', 20]] ],
            ['CareersOffice', [['StudentsUnion', 15], ['Chaplin', 20], ['Entrance2', 10]] ],
            ['MedicalSuites', [['StudentServices', 20]] ],
            ['FirstFloor1', [['Entrance1', 30]] ],
            ['FirstFloor2', [['Entrance2', 30]] ]
        ];


Instructions_Dic[0] = path_instruction_dic0;
//Instructions_Dic[1] = path_instruction_dic1;
//Instructions_Dic[2] = path_instruction_dic3;



Connections_Dic[0] = connection0;
//Connections_Dic[1] = connection1;
//Connections_Dic[2] = connection2;