
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'nonassocSEMICOLONrightASSIGNleftNOT_EQUALnonassocLTLEGTGEleftADDSUBleftMULDIVleftLPARENRPARENleftLBRACKRBRACKleftLBRACERBRACEADD AND ASSIGN CARGA CHAR COMMA COMMENT CORRELACIONA CTE_CH CTE_FLOAT CTE_INT CTE_STR DATAFRAME DESDE DISTRIBUCION DIV ENTONCES EQUAL ESCRIBE FLOAT FUNCION GE GT HACER HASTA HAZ ID INT LBRACE LBRACK LE LEE LPAREN LT MEDIA MEDIANA MIENTRAS MODA MUL NOT_EQUAL OR PRINCIPAL PROGRAMA RBRACE RBRACK REGRESA RPAREN SEMICOLON SI SINO STRING SUB TENDENCIA TWO_DOTS VAR VARIABLES VARIANZA VOIDprograma : PROGRAMA ID SEMICOLON var1 func1 principal pn_6_end\n    var1 : var\n         | empty\n    \n    func1 : funcion func1\n          | empty\n    principal : PRINCIPAL LPAREN RPAREN bloquevar : VAR var2var2 : type TWO_DOTS lista_ids var3\n    var3 : var2\n         | empty\n    \n    type : tipo_simple\n         | tipo_compuesto\n    funcion : FUNCION tipo_fun ID pn_3_addFunction LPAREN parametros RPAREN pn_5_updateContParams var1 bloque\n    tipo_fun : VOID pn_1_setCurrentType\n             | tipo_simple\n    \n    parametros : param\n               | empty\n    param : tipo_simple ID pn_4_params param1\n    param1 : COMMA param\n           | empty\n    \n    tipo_simple : INT pn_1_setCurrentType\n                | FLOAT pn_1_setCurrentType\n                | CHAR pn_1_setCurrentType\n    \n    tipo_compuesto : DATAFRAME pn_1_setCurrentType\n                   | STRING pn_1_setCurrentType\n    lista_ids : lista SEMICOLONlista : ID dd pn_2_addVariable lista1\n    dd : dim_dec\n       | empty\n    \n    lista1 : COMMA lista\n           | empty\n    dim_dec : LBRACK CTE_INT RBRACK pn_7_decRenglones dim_dec1\n    dim_dec1 : LBRACK CTE_INT RBRACK pn_8_decColumnas\n             | empty\n    dim_index : LBRACK exp RBRACK dim_index1\n    dim_index1 : LBRACK exp RBRACK\n               | empty\n    bloque : LBRACE est RBRACE\n    est : estatutos est\n        | empty\n    \n    estatutos : asignacion\n              | llamada\n              | retorno\n              | lectura\n              | escritura\n              | carga_datos\n              | decision\n              | condicional\n              | no_condicional\n              | funciones_especiales_void\n    asignacion : variable ASSIGN pnQuadGenSec1 asig\n    asig : llamada\n         | exp SEMICOLON pnQuadGenSec2\n    variable : ID pnQuadGenExp1 di\n    di : dim_index\n       | empty\n    llamada :  ID LPAREN llamada1 RPAREN SEMICOLON\n    llamada1 : exp llamada2\n             | empty\n    \n    llamada2 : COMMA llamada1\n             | empty\n    retorno : REGRESA LPAREN exp RPAREN SEMICOLONlectura : LEE pnQuadGenSec3 LPAREN variable RPAREN SEMICOLON pnQuadGenSec4escritura : ESCRIBE pnQuadGenSec3 LPAREN esc RPAREN SEMICOLON pnQuadGenSec4esc : esc1 esc2\n    esc1 : exp\n         | CTE_STR\n    \n    esc2 : COMMA esc\n         | empty\n    carga_datos : CARGA LPAREN ID COMMA CTE_STR COMMA ca COMMA ca RPAREN SEMICOLON\n    ca : ID\n       | CTE_INT\n    decision : SI LPAREN expresion RPAREN pnQuadGenCond1 ENTONCES bloque sino pnQuadGenCond3\n    sino : SINO pnQuadGenCond2 bloque\n         | empty\n    condicional : MIENTRAS LPAREN expresion RPAREN HAZ bloqueno_condicional : DESDE variable ASSIGN exp HASTA exp HACER bloque\n    funciones_especiales_void : VARIABLES LPAREN ID COMMA ID COMMA ID RPAREN SEMICOLON\n                              | fev LPAREN ID COMMA v_exp RPAREN SEMICOLON\n    \n    fev : DISTRIBUCION\n        | TENDENCIA\n    \n    funciones_especiales : fe LPAREN ID COMMA v_exp RPAREN\n                         | CORRELACIONA LPAREN ID COMMA v_exp COMMA v_exp RPAREN\n    \n    fe : MEDIA\n       | MEDIANA\n       | MODA\n       | VARIANZA\n    v_exp : VARIABLES LBRACK exp RBRACK\n    var_cte : CTE_INT pnQuadGenExp1\n            | CTE_FLOAT pnQuadGenExp1\n            | CTE_CH \n    expresion : mega_exp expresion1\n    expresion1 : ASSIGN expresion\n               | empty\n    mega_exp : super_exp meg\n    meg : op_l pnQuadGenExp10 mega_exp pnQuadGenExp11\n        | empty\n    \n    op_l : AND\n         | OR\n    super_exp : exp sp\n    sp : op_r  exp pnQuadGenExp9\n       | empty\n    \n    op_r : LT pnQuadGenExp8\n         | GT pnQuadGenExp8\n         | LE pnQuadGenExp8\n         | GE pnQuadGenExp8\n         | NOT_EQUAL pnQuadGenExp8\n         | EQUAL pnQuadGenExp8\n    exp : termino pnQuadGenExp4 exp1\n    exp1 : op_a exp\n         | empty\n    \n    op_a : ADD pnQuadGenExp2\n         | SUB pnQuadGenExp2\n    termino : factor pnQuadGenExp5 term\n    term : op_a1 termino\n         | empty\n    \n    op_a1 : MUL pnQuadGenExp3\n          | DIV pnQuadGenExp3\n    \n    factor : var_cte\n           | LPAREN pnQuadGenExp6 exp RPAREN pnQuadGenExp7\n           | variable\n           | llamada\n           | funciones_especiales\n    empty :\n    pn_1_setCurrentType :\n    \n    pn_2_addVariable : \n    \n    pn_3_addFunction : \n    \n    pn_4_params :\n    \n    pn_5_updateContParams :  \n    \n    pn_6_end :\n    \n    pn_7_decRenglones :\n    \n    pn_8_decColumnas : \n    \n    pnQuadGenExp1 : \n    \n    pnQuadGenExp2 : \n    \n    pnQuadGenExp3 : \n    \n    pnQuadGenExp4 : \n    \n    pnQuadGenExp5 : \n    \n    pnQuadGenExp6 : \n    \n    pnQuadGenExp7 : \n    \n    pnQuadGenExp8 : \n    \n    pnQuadGenExp9 : \n    \n    pnQuadGenExp10 : \n    \n    pnQuadGenExp11 : \n    \n    pnQuadGenSec1 : \n    \n    pnQuadGenSec2 : \n    \n    pnQuadGenSec3 : \n    \n    pnQuadGenSec4 : \n    \n    pnQuadGenCond1 :\n    \n    pnQuadGenCond2 :\n    \n    pnQuadGenCond3 :\n    '
    
_lr_action_items = {'HAZ':([165,],[215,]),'SUB':([73,100,110,111,112,115,117,118,124,125,126,128,136,137,139,152,158,164,166,185,207,210,232,233,249,251,260,261,273,284,288,299,],[-133,-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,205,-124,-89,-90,-122,-114,-116,-124,-57,-115,-139,-37,-35,-120,-82,-36,-83,]),'VOID':([10,],[25,]),'EQUAL':([100,110,111,112,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,201,204,207,210,232,233,244,249,251,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,173,-55,-54,-56,-124,-124,-89,-90,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,-82,-36,-83,]),'CARGA':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[56,-47,-42,-43,-48,56,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'CHAR':([6,10,38,46,53,195,],[19,19,19,-26,19,19,]),'SINO':([93,282,],[-38,290,]),'CORRELACIONA':([91,92,99,101,104,123,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[129,129,-144,129,129,-138,129,129,129,129,-98,-142,-99,129,129,-140,-140,-140,129,-140,-140,-140,129,-134,129,-134,129,-135,-135,129,-104,-107,-106,-108,-103,-105,129,129,-112,-113,-117,-118,129,129,]),'CTE_CH':([91,92,99,101,104,123,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[111,111,-144,111,111,-138,111,111,111,111,-98,-142,-99,111,111,-140,-140,-140,111,-140,-140,-140,111,-134,111,-134,111,-135,-135,111,-104,-107,-106,-108,-103,-105,111,111,-112,-113,-117,-118,111,111,]),'MUL':([73,100,110,111,115,117,118,124,125,126,128,136,137,139,158,164,166,185,232,233,251,260,261,273,284,288,299,],[-133,-124,-119,-91,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,208,-89,-90,-122,-124,-57,-139,-37,-35,-120,-82,-36,-83,]),'TENDENCIA':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[58,-47,-42,-43,-48,58,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'DIV':([73,100,110,111,115,117,118,124,125,126,128,136,137,139,158,164,166,185,232,233,251,260,261,273,284,288,299,],[-133,-124,-119,-91,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,209,-89,-90,-122,-124,-57,-139,-37,-35,-120,-82,-36,-83,]),'RBRACE':([51,60,61,63,65,66,68,69,71,74,76,78,80,81,93,96,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[-124,93,-47,-42,-43,-40,-48,-124,-50,-49,-41,-44,-46,-45,-38,-39,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'NOT_EQUAL':([100,110,111,112,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,201,204,207,210,232,233,244,249,251,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,169,-55,-54,-56,-124,-124,-89,-90,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,-82,-36,-83,]),'RPAREN':([34,53,83,84,85,97,100,101,105,110,111,112,114,115,117,118,121,124,125,126,127,128,130,131,136,137,139,140,141,142,145,146,152,154,157,158,159,160,164,166,170,176,178,179,180,181,189,190,191,192,196,197,201,204,207,210,212,214,220,226,228,232,233,234,237,239,244,246,249,251,254,256,260,261,269,270,271,272,273,276,284,288,289,293,294,299,],[41,-124,-16,106,-17,-133,-124,-124,-128,-119,-91,-136,-124,-123,-122,-137,-124,-121,-133,-133,165,-133,-124,177,-55,-54,-56,188,-59,-124,194,-124,-124,-95,-97,-124,-92,-94,-89,-90,-100,-102,225,-124,-67,-66,-58,-124,-61,235,-18,-20,-109,-111,-114,-116,-93,251,-141,-65,-69,-124,-57,-60,265,-19,-110,-143,-115,-139,-101,-68,-37,-35,-72,-71,-96,284,-120,286,-82,-36,-88,298,299,-83,]),'SEMICOLON':([3,39,40,47,49,50,54,73,86,88,89,100,107,108,110,111,112,115,117,118,124,125,126,128,136,137,139,148,150,152,158,164,166,177,185,186,188,201,204,207,210,225,232,233,235,241,244,249,251,260,261,265,267,273,284,286,288,298,299,],[4,46,-124,-126,-28,-29,-124,-133,-27,-31,-131,-124,-30,-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,-32,-34,-124,-124,-89,-90,224,-122,231,233,-109,-111,-114,-116,255,-124,-57,263,-132,-110,-115,-139,-37,-35,281,-33,-120,-82,295,-36,301,-83,]),'VARIABLES':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,193,224,231,233,250,252,253,255,259,263,275,279,281,282,285,287,291,292,295,297,300,301,],[67,-47,-42,-43,-48,67,-50,-49,-41,-44,-46,-45,-38,-51,-52,236,-62,-145,-57,236,-76,236,-147,-53,-147,-64,-63,-79,-124,236,-77,-150,-75,-78,-73,-74,-70,]),'GE':([100,110,111,112,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,201,204,207,210,232,233,244,249,251,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,171,-55,-54,-56,-124,-124,-89,-90,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,-82,-36,-83,]),'DATAFRAME':([6,38,46,],[18,18,-26,]),'ESCRIBE':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[62,-47,-42,-43,-48,62,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'MODA':([91,92,99,101,104,123,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[116,116,-144,116,116,-138,116,116,116,116,-98,-142,-99,116,116,-140,-140,-140,116,-140,-140,-140,116,-134,116,-134,116,-135,-135,116,-104,-107,-106,-108,-103,-105,116,116,-112,-113,-117,-118,116,116,]),'LT':([100,110,111,112,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,201,204,207,210,232,233,244,249,251,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,174,-55,-54,-56,-124,-124,-89,-90,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,-82,-36,-83,]),'COMMA':([40,47,49,50,54,89,100,105,108,109,110,111,112,115,117,118,124,125,126,128,133,136,137,139,142,144,146,148,150,152,158,164,166,179,180,181,200,201,204,207,210,213,216,229,232,233,241,244,249,251,260,261,267,268,269,270,273,274,284,288,289,299,],[-124,-126,-28,-29,87,-131,-124,-128,-124,151,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,182,-55,-54,-56,190,193,195,-32,-34,-124,-124,-89,-90,227,-67,-66,242,-109,-111,-114,-116,250,253,257,-124,-57,-132,-110,-115,-139,-37,-35,-33,283,-72,-71,-120,285,-82,-36,-88,-83,]),'DISTRIBUCION':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[64,-47,-42,-43,-48,64,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'MEDIANA':([91,92,99,101,104,123,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[119,119,-144,119,119,-138,119,119,119,119,-98,-142,-99,119,119,-140,-140,-140,119,-140,-140,-140,119,-134,119,-134,119,-135,-135,119,-104,-107,-106,-108,-103,-105,119,119,-112,-113,-117,-118,119,119,]),'ASSIGN':([72,73,97,98,100,110,111,112,114,115,117,118,121,124,125,126,128,130,136,137,139,152,154,157,158,164,166,170,176,201,204,207,210,220,232,233,244,246,249,251,254,260,261,271,273,284,288,299,],[99,-133,-133,134,-124,-119,-91,-136,-124,-123,-122,-137,161,-121,-133,-133,-133,-124,-55,-54,-56,-124,-95,-97,-124,-89,-90,-100,-102,-109,-111,-114,-116,-141,-124,-57,-110,-143,-115,-139,-101,-37,-35,-96,-120,-82,-36,-83,]),'$end':([1,23,35,52,93,],[0,-130,-1,-6,-38,]),'HACER':([100,110,111,112,115,117,118,124,125,126,128,136,137,139,152,158,164,166,201,204,207,210,232,233,244,249,251,258,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,-124,-124,-89,-90,-109,-111,-114,-116,-124,-57,-110,-115,-139,277,-37,-35,-120,-82,-36,-83,]),'GT':([100,110,111,112,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,201,204,207,210,232,233,244,249,251,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,168,-55,-54,-56,-124,-124,-89,-90,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,-82,-36,-83,]),'STRING':([6,38,46,],[15,15,-26,]),'MEDIA':([91,92,99,101,104,123,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[120,120,-144,120,120,-138,120,120,120,120,-98,-142,-99,120,120,-140,-140,-140,120,-140,-140,-140,120,-134,120,-134,120,-135,-135,120,-104,-107,-106,-108,-103,-105,120,120,-112,-113,-117,-118,120,120,]),'REGRESA':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[59,-47,-42,-43,-48,59,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'RBRACK':([55,100,110,111,112,115,117,118,124,125,126,128,136,137,139,152,158,164,166,187,199,201,204,207,210,232,233,244,249,251,260,261,273,278,280,284,288,299,],[89,-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,-124,-124,-89,-90,232,241,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,288,289,-82,-36,-83,]),'HASTA':([100,110,111,112,115,117,118,124,125,126,128,136,137,139,152,158,164,166,183,201,204,207,210,232,233,244,249,251,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,-124,-124,-89,-90,230,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,-82,-36,-83,]),'MIENTRAS':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[57,-47,-42,-43,-48,57,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'ADD':([73,100,110,111,112,115,117,118,124,125,126,128,136,137,139,152,158,164,166,185,207,210,232,233,249,251,260,261,273,284,288,299,],[-133,-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,-55,-54,-56,202,-124,-89,-90,-122,-114,-116,-124,-57,-115,-139,-37,-35,-120,-82,-36,-83,]),'LE':([100,110,111,112,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,201,204,207,210,232,233,244,249,251,260,261,273,284,288,299,],[-124,-119,-91,-136,-123,-122,-137,-121,-133,-133,-133,175,-55,-54,-56,-124,-124,-89,-90,-109,-111,-114,-116,-124,-57,-110,-115,-139,-37,-35,-120,-82,-36,-83,]),'DESDE':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[70,-47,-42,-43,-48,70,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'LPAREN':([22,37,42,56,57,58,59,62,64,67,73,75,77,79,91,92,94,99,101,102,104,113,116,119,120,122,123,126,129,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[34,-127,53,90,91,-81,92,-146,-80,95,101,-146,103,104,123,123,132,-144,123,143,123,-87,-86,-85,-84,162,-138,101,167,123,123,123,123,-98,-142,-99,123,123,-140,-140,-140,123,-140,-140,-140,123,-134,123,-134,123,-135,-135,123,-104,-107,-106,-108,-103,-105,123,123,-112,-113,-117,-118,123,123,]),'VAR':([4,106,147,],[6,-129,6,]),'CTE_INT':([48,91,92,99,101,104,123,132,134,135,138,149,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,242,243,245,247,248,262,264,283,],[55,125,125,-144,125,125,-138,125,125,125,125,199,-98,-142,-99,125,125,-140,-140,-140,125,-140,-140,-140,125,-134,125,-134,125,-135,-135,125,-104,-107,-106,-108,-103,-105,125,125,269,-112,-113,-117,-118,125,125,269,]),'ID':([2,14,19,21,24,25,26,28,31,32,33,36,51,61,63,65,68,69,70,71,74,76,78,80,81,82,87,90,91,92,93,95,99,101,103,104,123,132,134,135,138,143,153,155,156,161,162,163,167,168,169,171,172,173,174,175,182,184,185,190,202,203,205,206,208,209,211,217,218,219,221,222,223,224,227,230,231,233,242,243,245,247,248,252,255,257,259,262,263,264,275,279,281,282,283,287,291,292,295,297,300,301,],[3,-125,-125,-125,-15,-125,37,-22,-23,40,-21,-14,73,-47,-42,-43,-48,73,97,-50,-49,-41,-44,-46,-45,105,40,109,126,126,-38,133,-144,126,144,126,-138,126,126,73,126,97,-98,-142,-99,126,213,126,216,-140,-140,-140,126,-140,-140,-140,229,-51,-52,126,-134,126,-134,126,-135,-135,126,-104,-107,-106,-108,-103,-105,-62,126,126,-145,-57,270,-112,-113,-117,-118,-76,-147,276,-53,126,-147,126,-64,-63,-79,-124,270,-77,-150,-75,-78,-73,-74,-70,]),'FUNCION':([4,5,7,8,11,16,38,43,44,45,46,93,240,],[-124,10,-2,-3,10,-7,-124,-8,-9,-10,-26,-38,-13,]),'AND':([100,110,111,112,114,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,170,176,201,204,207,210,220,232,233,244,249,251,254,260,261,273,284,288,299,],[-124,-119,-91,-136,153,-123,-122,-137,-121,-133,-133,-133,-124,-55,-54,-56,-124,-124,-89,-90,-100,-102,-109,-111,-114,-116,-141,-124,-57,-110,-115,-139,-101,-37,-35,-120,-82,-36,-83,]),'LBRACE':([7,8,16,38,41,43,44,45,46,106,147,198,215,266,277,290,296,],[-2,-3,-7,-124,51,-8,-9,-10,-26,-129,-124,51,51,51,51,-149,51,]),'LEE':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[75,-47,-42,-43,-48,75,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'VARIANZA':([91,92,99,101,104,123,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[113,113,-144,113,113,-138,113,113,113,113,-98,-142,-99,113,113,-140,-140,-140,113,-140,-140,-140,113,-134,113,-134,113,-135,-135,113,-104,-107,-106,-108,-103,-105,113,113,-112,-113,-117,-118,113,113,]),'CTE_STR':([132,151,227,],[180,200,180,]),'INT':([6,10,38,46,53,195,],[21,21,21,-26,21,21,]),'FLOAT':([6,10,38,46,53,195,],[14,14,14,-26,14,14,]),'CTE_FLOAT':([91,92,99,101,104,123,132,134,135,138,153,155,156,161,163,168,169,171,172,173,174,175,190,202,203,205,206,208,209,211,217,218,219,221,222,223,227,230,243,245,247,248,262,264,],[128,128,-144,128,128,-138,128,128,128,128,-98,-142,-99,128,128,-140,-140,-140,128,-140,-140,-140,128,-134,128,-134,128,-135,-135,128,-104,-107,-106,-108,-103,-105,128,128,-112,-113,-117,-118,128,128,]),'LBRACK':([40,73,89,97,100,108,126,232,236,],[48,-133,-131,-133,138,149,-133,262,264,]),'ENTONCES':([194,238,],[-148,266,]),'TWO_DOTS':([13,14,15,17,18,19,20,21,28,29,30,31,33,],[-12,-125,-125,-11,-125,-125,32,-125,-22,-25,-24,-23,-21,]),'SI':([51,61,63,65,68,69,71,74,76,78,80,81,93,184,185,224,231,233,252,255,259,263,275,279,281,282,287,291,292,295,297,300,301,],[79,-47,-42,-43,-48,79,-50,-49,-41,-44,-46,-45,-38,-51,-52,-62,-145,-57,-76,-147,-53,-147,-64,-63,-79,-124,-77,-150,-75,-78,-73,-74,-70,]),'PROGRAMA':([0,],[2,]),'OR':([100,110,111,112,114,115,117,118,124,125,126,128,130,136,137,139,152,158,164,166,170,176,201,204,207,210,220,232,233,244,249,251,254,260,261,273,284,288,299,],[-124,-119,-91,-136,156,-123,-122,-137,-121,-133,-133,-133,-124,-55,-54,-56,-124,-124,-89,-90,-100,-102,-109,-111,-114,-116,-141,-124,-57,-110,-115,-139,-101,-37,-35,-120,-82,-36,-83,]),'PRINCIPAL':([4,5,7,8,9,11,12,16,27,38,43,44,45,46,93,240,],[-124,-124,-2,-3,22,-124,-5,-7,-4,-124,-8,-9,-10,-26,-38,-13,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'bloque':([41,198,215,266,277,296,],[52,240,252,282,287,300,]),'principal':([9,],[23,]),'funciones_especiales':([91,92,101,104,132,134,135,138,161,163,172,190,203,206,211,227,230,262,264,],[115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,]),'param':([53,195,],[83,239,]),'pnQuadGenCond3':([291,],[297,]),'pnQuadGenCond2':([290,],[296,]),'pnQuadGenCond1':([194,],[238,]),'factor':([91,92,101,104,132,134,135,138,161,163,172,190,203,206,211,227,230,262,264,],[118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,]),'dim_dec':([40,],[49,]),'tipo_compuesto':([6,38,],[13,13,]),'func1':([5,11,],[9,27,]),'var1':([4,147,],[5,198,]),'var3':([38,],[43,]),'di':([100,],[137,]),'condicional':([51,69,],[68,68,]),'tipo_fun':([10,],[26,]),'pnQuadGenExp11':([246,],[271,]),'estatutos':([51,69,],[69,69,]),'expresion':([91,104,161,],[127,145,212,]),'term':([158,],[207,]),'pnQuadGenExp7':([251,],[273,]),'parametros':([53,],[84,]),'lista1':([54,],[86,]),'carga_datos':([51,69,],[80,80,]),'op_a1':([158,],[211,]),'pn_1_setCurrentType':([14,15,18,19,21,25,],[28,29,30,31,33,36,]),'var_cte':([91,92,101,104,132,134,135,138,161,163,172,190,203,206,211,227,230,262,264,],[110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,]),'super_exp':([91,104,161,206,],[114,114,114,114,]),'dim_index':([100,],[136,]),'est':([51,69,],[60,96,]),'asig':([135,],[184,]),'decision':([51,69,],[61,61,]),'lista_ids':([32,],[38,]),'llamada':([51,69,91,92,101,104,132,134,135,138,161,163,172,190,203,206,211,227,230,262,264,],[63,63,117,117,117,117,117,117,185,117,117,117,117,117,117,117,117,117,117,117,117,]),'esc':([132,227,],[178,256,]),'lectura':([51,69,],[78,78,]),'meg':([114,],[154,]),'sino':([282,],[291,]),'funciones_especiales_void':([51,69,],[71,71,]),'pn_2_addVariable':([47,],[54,]),'dim_index1':([232,],[261,]),'fe':([91,92,101,104,132,134,135,138,161,163,172,190,203,206,211,227,230,262,264,],[122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,]),'pn_3_addFunction':([37,],[42,]),'tipo_simple':([6,10,38,53,195,],[17,24,17,82,82,]),'ca':([242,283,],[268,293,]),'termino':([91,92,101,104,132,134,135,138,161,163,172,190,203,206,211,227,230,262,264,],[112,112,112,112,112,112,112,112,112,112,112,112,112,112,249,112,112,112,112,]),'exp1':([152,],[201,]),'fev':([51,69,],[77,77,]),'var':([4,147,],[7,7,]),'pn_5_updateContParams':([106,],[147,]),'type':([6,38,],[20,20,]),'empty':([4,5,11,38,40,51,53,54,69,100,101,108,114,121,130,142,146,147,152,158,179,190,232,282,],[8,12,12,45,50,66,85,88,66,139,141,150,157,160,176,191,197,8,204,210,228,141,260,292,]),'expresion1':([121,],[159,]),'dim_dec1':([108,],[148,]),'pnQuadGenSec2':([231,],[259,]),'pnQuadGenSec1':([99,],[135,]),'op_r':([130,],[172,]),'pnQuadGenSec4':([255,263,],[275,279,]),'op_l':([114,],[155,]),'lista':([32,87,],[39,107,]),'op_a':([152,],[203,]),'no_condicional':([51,69,],[74,74,]),'pnQuadGenExp1':([73,97,125,126,128,],[100,100,164,100,166,]),'pnQuadGenExp3':([208,209,],[247,248,]),'pnQuadGenExp2':([202,205,],[243,245,]),'pnQuadGenExp5':([118,],[158,]),'pnQuadGenExp4':([112,],[152,]),'asignacion':([51,69,],[76,76,]),'pnQuadGenExp6':([123,],[163,]),'pnQuadGenExp9':([220,],[254,]),'pnQuadGenExp8':([168,169,171,173,174,175,],[217,218,219,221,222,223,]),'param1':([146,],[196,]),'llamada2':([142,],[189,]),'llamada1':([101,190,],[140,234,]),'v_exp':([193,250,253,285,],[237,272,274,294,]),'pn_8_decColumnas':([241,],[267,]),'var2':([6,38,],[16,44,]),'pnQuadGenSec3':([62,75,],[94,102,]),'retorno':([51,69,],[65,65,]),'pnQuadGenExp10':([155,],[206,]),'dd':([40,],[47,]),'funcion':([5,11,],[11,11,]),'pn_6_end':([23,],[35,]),'escritura':([51,69,],[81,81,]),'esc1':([132,227,],[179,179,]),'esc2':([179,],[226,]),'mega_exp':([91,104,161,206,],[121,121,121,246,]),'variable':([51,69,70,91,92,101,104,132,134,135,138,143,161,163,172,190,203,206,211,227,230,262,264,],[72,72,98,124,124,124,124,124,124,124,124,192,124,124,124,124,124,124,124,124,124,124,124,]),'sp':([130,],[170,]),'pn_4_params':([105,],[146,]),'programa':([0,],[1,]),'exp':([91,92,101,104,132,134,135,138,161,163,172,190,203,206,227,230,262,264,],[130,131,142,130,181,183,186,187,130,214,220,142,244,130,181,258,278,280,]),'pn_7_decRenglones':([89,],[108,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> PROGRAMA ID SEMICOLON var1 func1 principal pn_6_end','programa',7,'p_programa','parser.py',74),
  ('var1 -> var','var1',1,'p_var1','parser.py',79),
  ('var1 -> empty','var1',1,'p_var1','parser.py',80),
  ('func1 -> funcion func1','func1',2,'p_func1','parser.py',86),
  ('func1 -> empty','func1',1,'p_func1','parser.py',87),
  ('principal -> PRINCIPAL LPAREN RPAREN bloque','principal',4,'p_principal','parser.py',92),
  ('var -> VAR var2','var',2,'p_var','parser.py',97),
  ('var2 -> type TWO_DOTS lista_ids var3','var2',4,'p_var2','parser.py',101),
  ('var3 -> var2','var3',1,'p_var3','parser.py',106),
  ('var3 -> empty','var3',1,'p_var3','parser.py',107),
  ('type -> tipo_simple','type',1,'p_type','parser.py',113),
  ('type -> tipo_compuesto','type',1,'p_type','parser.py',114),
  ('funcion -> FUNCION tipo_fun ID pn_3_addFunction LPAREN parametros RPAREN pn_5_updateContParams var1 bloque','funcion',10,'p_funcion','parser.py',119),
  ('tipo_fun -> VOID pn_1_setCurrentType','tipo_fun',2,'p_tipo_fun','parser.py',124),
  ('tipo_fun -> tipo_simple','tipo_fun',1,'p_tipo_fun','parser.py',125),
  ('parametros -> param','parametros',1,'p_parametros','parser.py',131),
  ('parametros -> empty','parametros',1,'p_parametros','parser.py',132),
  ('param -> tipo_simple ID pn_4_params param1','param',4,'p_param','parser.py',137),
  ('param1 -> COMMA param','param1',2,'p_param1','parser.py',142),
  ('param1 -> empty','param1',1,'p_param1','parser.py',143),
  ('tipo_simple -> INT pn_1_setCurrentType','tipo_simple',2,'p_tipo_simple','parser.py',149),
  ('tipo_simple -> FLOAT pn_1_setCurrentType','tipo_simple',2,'p_tipo_simple','parser.py',150),
  ('tipo_simple -> CHAR pn_1_setCurrentType','tipo_simple',2,'p_tipo_simple','parser.py',151),
  ('tipo_compuesto -> DATAFRAME pn_1_setCurrentType','tipo_compuesto',2,'p_tipo_compuesto','parser.py',156),
  ('tipo_compuesto -> STRING pn_1_setCurrentType','tipo_compuesto',2,'p_tipo_compuesto','parser.py',157),
  ('lista_ids -> lista SEMICOLON','lista_ids',2,'p_lista_ids','parser.py',162),
  ('lista -> ID dd pn_2_addVariable lista1','lista',4,'p_lista','parser.py',165),
  ('dd -> dim_dec','dd',1,'p_dd','parser.py',169),
  ('dd -> empty','dd',1,'p_dd','parser.py',170),
  ('lista1 -> COMMA lista','lista1',2,'p_lista1','parser.py',175),
  ('lista1 -> empty','lista1',1,'p_lista1','parser.py',176),
  ('dim_dec -> LBRACK CTE_INT RBRACK pn_7_decRenglones dim_dec1','dim_dec',5,'p_dim_dec','parser.py',181),
  ('dim_dec1 -> LBRACK CTE_INT RBRACK pn_8_decColumnas','dim_dec1',4,'p_dim_dec1','parser.py',185),
  ('dim_dec1 -> empty','dim_dec1',1,'p_dim_dec1','parser.py',186),
  ('dim_index -> LBRACK exp RBRACK dim_index1','dim_index',4,'p_dim_index','parser.py',190),
  ('dim_index1 -> LBRACK exp RBRACK','dim_index1',3,'p_dim_index1','parser.py',194),
  ('dim_index1 -> empty','dim_index1',1,'p_dim_index1','parser.py',195),
  ('bloque -> LBRACE est RBRACE','bloque',3,'p_bloque','parser.py',201),
  ('est -> estatutos est','est',2,'p_est','parser.py',206),
  ('est -> empty','est',1,'p_est','parser.py',207),
  ('estatutos -> asignacion','estatutos',1,'p_estatutos','parser.py',213),
  ('estatutos -> llamada','estatutos',1,'p_estatutos','parser.py',214),
  ('estatutos -> retorno','estatutos',1,'p_estatutos','parser.py',215),
  ('estatutos -> lectura','estatutos',1,'p_estatutos','parser.py',216),
  ('estatutos -> escritura','estatutos',1,'p_estatutos','parser.py',217),
  ('estatutos -> carga_datos','estatutos',1,'p_estatutos','parser.py',218),
  ('estatutos -> decision','estatutos',1,'p_estatutos','parser.py',219),
  ('estatutos -> condicional','estatutos',1,'p_estatutos','parser.py',220),
  ('estatutos -> no_condicional','estatutos',1,'p_estatutos','parser.py',221),
  ('estatutos -> funciones_especiales_void','estatutos',1,'p_estatutos','parser.py',222),
  ('asignacion -> variable ASSIGN pnQuadGenSec1 asig','asignacion',4,'p_asignacion','parser.py',229),
  ('asig -> llamada','asig',1,'p_asig','parser.py',233),
  ('asig -> exp SEMICOLON pnQuadGenSec2','asig',3,'p_asig','parser.py',234),
  ('variable -> ID pnQuadGenExp1 di','variable',3,'p_variable','parser.py',237),
  ('di -> dim_index','di',1,'p_di','parser.py',241),
  ('di -> empty','di',1,'p_di','parser.py',242),
  ('llamada -> ID LPAREN llamada1 RPAREN SEMICOLON','llamada',5,'p_llamada','parser.py',246),
  ('llamada1 -> exp llamada2','llamada1',2,'p_llamada1','parser.py',250),
  ('llamada1 -> empty','llamada1',1,'p_llamada1','parser.py',251),
  ('llamada2 -> COMMA llamada1','llamada2',2,'p_llamada2','parser.py',256),
  ('llamada2 -> empty','llamada2',1,'p_llamada2','parser.py',257),
  ('retorno -> REGRESA LPAREN exp RPAREN SEMICOLON','retorno',5,'p_retorno','parser.py',261),
  ('lectura -> LEE pnQuadGenSec3 LPAREN variable RPAREN SEMICOLON pnQuadGenSec4','lectura',7,'p_lectura','parser.py',264),
  ('escritura -> ESCRIBE pnQuadGenSec3 LPAREN esc RPAREN SEMICOLON pnQuadGenSec4','escritura',7,'p_escritura','parser.py',267),
  ('esc -> esc1 esc2','esc',2,'p_esc','parser.py',270),
  ('esc1 -> exp','esc1',1,'p_esc1','parser.py',274),
  ('esc1 -> CTE_STR','esc1',1,'p_esc1','parser.py',275),
  ('esc2 -> COMMA esc','esc2',2,'p_esc2','parser.py',279),
  ('esc2 -> empty','esc2',1,'p_esc2','parser.py',280),
  ('carga_datos -> CARGA LPAREN ID COMMA CTE_STR COMMA ca COMMA ca RPAREN SEMICOLON','carga_datos',11,'p_carga_datos','parser.py',284),
  ('ca -> ID','ca',1,'p_ca','parser.py',288),
  ('ca -> CTE_INT','ca',1,'p_ca','parser.py',289),
  ('decision -> SI LPAREN expresion RPAREN pnQuadGenCond1 ENTONCES bloque sino pnQuadGenCond3','decision',9,'p_decision','parser.py',294),
  ('sino -> SINO pnQuadGenCond2 bloque','sino',3,'p_sino','parser.py',298),
  ('sino -> empty','sino',1,'p_sino','parser.py',299),
  ('condicional -> MIENTRAS LPAREN expresion RPAREN HAZ bloque','condicional',6,'p_condicional','parser.py',303),
  ('no_condicional -> DESDE variable ASSIGN exp HASTA exp HACER bloque','no_condicional',8,'p_no_condicional','parser.py',306),
  ('funciones_especiales_void -> VARIABLES LPAREN ID COMMA ID COMMA ID RPAREN SEMICOLON','funciones_especiales_void',9,'p_funciones_especiales_void','parser.py',311),
  ('funciones_especiales_void -> fev LPAREN ID COMMA v_exp RPAREN SEMICOLON','funciones_especiales_void',7,'p_funciones_especiales_void','parser.py',312),
  ('fev -> DISTRIBUCION','fev',1,'p_fev','parser.py',316),
  ('fev -> TENDENCIA','fev',1,'p_fev','parser.py',317),
  ('funciones_especiales -> fe LPAREN ID COMMA v_exp RPAREN','funciones_especiales',6,'p_funciones_especiales','parser.py',322),
  ('funciones_especiales -> CORRELACIONA LPAREN ID COMMA v_exp COMMA v_exp RPAREN','funciones_especiales',8,'p_funciones_especiales','parser.py',323),
  ('fe -> MEDIA','fe',1,'p_fe','parser.py',327),
  ('fe -> MEDIANA','fe',1,'p_fe','parser.py',328),
  ('fe -> MODA','fe',1,'p_fe','parser.py',329),
  ('fe -> VARIANZA','fe',1,'p_fe','parser.py',330),
  ('v_exp -> VARIABLES LBRACK exp RBRACK','v_exp',4,'p_v_exp','parser.py',333),
  ('var_cte -> CTE_INT pnQuadGenExp1','var_cte',2,'p_var_cte','parser.py',340),
  ('var_cte -> CTE_FLOAT pnQuadGenExp1','var_cte',2,'p_var_cte','parser.py',341),
  ('var_cte -> CTE_CH','var_cte',1,'p_var_cte','parser.py',342),
  ('expresion -> mega_exp expresion1','expresion',2,'p_expresion','parser.py',348),
  ('expresion1 -> ASSIGN expresion','expresion1',2,'p_expresion1','parser.py',352),
  ('expresion1 -> empty','expresion1',1,'p_expresion1','parser.py',353),
  ('mega_exp -> super_exp meg','mega_exp',2,'p_mega_exp','parser.py',357),
  ('meg -> op_l pnQuadGenExp10 mega_exp pnQuadGenExp11','meg',4,'p_meg','parser.py',361),
  ('meg -> empty','meg',1,'p_meg','parser.py',362),
  ('op_l -> AND','op_l',1,'p_op_l','parser.py',366),
  ('op_l -> OR','op_l',1,'p_op_l','parser.py',367),
  ('super_exp -> exp sp','super_exp',2,'p_super_exp','parser.py',371),
  ('sp -> op_r exp pnQuadGenExp9','sp',3,'p_sp','parser.py',375),
  ('sp -> empty','sp',1,'p_sp','parser.py',376),
  ('op_r -> LT pnQuadGenExp8','op_r',2,'p_op_r','parser.py',380),
  ('op_r -> GT pnQuadGenExp8','op_r',2,'p_op_r','parser.py',381),
  ('op_r -> LE pnQuadGenExp8','op_r',2,'p_op_r','parser.py',382),
  ('op_r -> GE pnQuadGenExp8','op_r',2,'p_op_r','parser.py',383),
  ('op_r -> NOT_EQUAL pnQuadGenExp8','op_r',2,'p_op_r','parser.py',384),
  ('op_r -> EQUAL pnQuadGenExp8','op_r',2,'p_op_r','parser.py',385),
  ('exp -> termino pnQuadGenExp4 exp1','exp',3,'p_exp','parser.py',389),
  ('exp1 -> op_a exp','exp1',2,'p_exp1','parser.py',393),
  ('exp1 -> empty','exp1',1,'p_exp1','parser.py',394),
  ('op_a -> ADD pnQuadGenExp2','op_a',2,'p_op_a','parser.py',398),
  ('op_a -> SUB pnQuadGenExp2','op_a',2,'p_op_a','parser.py',399),
  ('termino -> factor pnQuadGenExp5 term','termino',3,'p_termino','parser.py',403),
  ('term -> op_a1 termino','term',2,'p_term','parser.py',407),
  ('term -> empty','term',1,'p_term','parser.py',408),
  ('op_a1 -> MUL pnQuadGenExp3','op_a1',2,'p_op_a1','parser.py',412),
  ('op_a1 -> DIV pnQuadGenExp3','op_a1',2,'p_op_a1','parser.py',413),
  ('factor -> var_cte','factor',1,'p_factor','parser.py',418),
  ('factor -> LPAREN pnQuadGenExp6 exp RPAREN pnQuadGenExp7','factor',5,'p_factor','parser.py',419),
  ('factor -> variable','factor',1,'p_factor','parser.py',420),
  ('factor -> llamada','factor',1,'p_factor','parser.py',421),
  ('factor -> funciones_especiales','factor',1,'p_factor','parser.py',422),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',427),
  ('pn_1_setCurrentType -> <empty>','pn_1_setCurrentType',0,'p_pn_1_setCurrentType','parser.py',540),
  ('pn_2_addVariable -> <empty>','pn_2_addVariable',0,'p_pn_2_addVariable','parser.py',547),
  ('pn_3_addFunction -> <empty>','pn_3_addFunction',0,'p_pn_3_addFunction','parser.py',563),
  ('pn_4_params -> <empty>','pn_4_params',0,'p_pn_4_params','parser.py',576),
  ('pn_5_updateContParams -> <empty>','pn_5_updateContParams',0,'p_pn_5_updateContParams','parser.py',589),
  ('pn_6_end -> <empty>','pn_6_end',0,'p_pn_6_end','parser.py',598),
  ('pn_7_decRenglones -> <empty>','pn_7_decRenglones',0,'p_pn_7_decRenglones','parser.py',604),
  ('pn_8_decColumnas -> <empty>','pn_8_decColumnas',0,'p_pn_8_decColumnas','parser.py',612),
  ('pnQuadGenExp1 -> <empty>','pnQuadGenExp1',0,'p_pnQuadGenExp1','parser.py',622),
  ('pnQuadGenExp2 -> <empty>','pnQuadGenExp2',0,'p_pnQuadGenExp2','parser.py',648),
  ('pnQuadGenExp3 -> <empty>','pnQuadGenExp3',0,'p_pnQuadGenExp3','parser.py',662),
  ('pnQuadGenExp4 -> <empty>','pnQuadGenExp4',0,'p_pnQuadGenExp4','parser.py',676),
  ('pnQuadGenExp5 -> <empty>','pnQuadGenExp5',0,'p_pnQuadGenExp5','parser.py',700),
  ('pnQuadGenExp6 -> <empty>','pnQuadGenExp6',0,'p_pnQuadGenExp6','parser.py',724),
  ('pnQuadGenExp7 -> <empty>','pnQuadGenExp7',0,'p_pnQuadGenExp7','parser.py',731),
  ('pnQuadGenExp8 -> <empty>','pnQuadGenExp8',0,'p_pnQuadGenExp8','parser.py',738),
  ('pnQuadGenExp9 -> <empty>','pnQuadGenExp9',0,'p_pnQuadGenExp9','parser.py',750),
  ('pnQuadGenExp10 -> <empty>','pnQuadGenExp10',0,'p_pnQuadGenExp10','parser.py',775),
  ('pnQuadGenExp11 -> <empty>','pnQuadGenExp11',0,'p_pnQuadGenExp11','parser.py',787),
  ('pnQuadGenSec1 -> <empty>','pnQuadGenSec1',0,'p_pnQuadGenSec1','parser.py',813),
  ('pnQuadGenSec2 -> <empty>','pnQuadGenSec2',0,'p_pnQuadGenSec2','parser.py',825),
  ('pnQuadGenSec3 -> <empty>','pnQuadGenSec3',0,'p_pnQuadGenSec3','parser.py',854),
  ('pnQuadGenSec4 -> <empty>','pnQuadGenSec4',0,'p_pnQuadGenSec4','parser.py',866),
  ('pnQuadGenCond1 -> <empty>','pnQuadGenCond1',0,'p_pnQuadGenCond1','parser.py',889),
  ('pnQuadGenCond2 -> <empty>','pnQuadGenCond2',0,'p_pnQuadGenCond2','parser.py',906),
  ('pnQuadGenCond3 -> <empty>','pnQuadGenCond3',0,'p_pnQuadGenCond3','parser.py',915),
]
