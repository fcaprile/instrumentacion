//// ****** THIS FILE IS AUTOGENERATED ******
////
////          >>>> DO NOT CHANGE <<<<
////
/// 
///  Filename; C:\Users\Publico.LABORATORIOS\Desktop\instrumentacion y control\arduino lantz\medir_y_enviar.py
///  Source class: Aparato
///  Generation timestamp: 2019-06-05T07:47:06.526517
///  Class code hash: b21abe376dc9b9ca0e8bcf26c5aec27723597706
///
/////////////////////////////////////////////////////////////


#include "inodriver_bridge.h"

SerialCommand sCmd;

void ok() {
  Serial.println("OK");
}

void error(const char* msg) {
  Serial.print("ERROR: ");
  Serial.println(msg);
}

void error_i(int errno) {
  Serial.print("ERROR: ");
  Serial.println(errno);
}

void bridge_loop() {
  while (Serial.available() > 0) {
    sCmd.readSerial();
  }
}

void bridge_setup() {
  //// Setup callbacks for SerialCommand commands

  // All commands might return
  //    ERROR: <error message>

  // All set commands return 
  //    OK 
  // if the operation is successfull

  // All parameters are ascii encoded strings
  sCmd.addCommand("INFO?", getInfo); 

  sCmd.setDefaultHandler(unrecognized); 


  // enable
  // <B> bool as string: True as "1", False as "0" 

  // Getter:
  //   ENABLE? 
  // Returns: <B> 
  sCmd.addCommand("ENABLE?", wrapperGet_ENABLE); 

  // Setter:
  //   ENABLE <B> 
  // Returns: OK or ERROR    
  sCmd.addCommand("ENABLE", wrapperSet_ENABLE); 

  // tension
  // <F> float as string 

  // Getter:
  //   Tension? 
  // Returns: <F> 
  sCmd.addCommand("Tension?", wrapperGet_Tension); 
}

//// Code 

void getInfo() {
  Serial.print("Aparato,");
  Serial.println(COMPILE_DATE_TIME);
}

void unrecognized(const char *command) {
  error("Unknown command");
}
//// Auto generated Feat and DictFeat Code
// COMMAND: ENABLE, FEAT: enable

void wrapperGet_ENABLE() { 
  Serial.println(get_ENABLE()); 
}; 


void wrapperSet_ENABLE() {
  char *arg;
  
  arg = sCmd.next();
  if (arg == NULL) {
    error("No value stated");
    return;
  }
  int value = atoi(arg);

  int err = set_ENABLE(value);
  if (err == 0) {
    ok();
  } else {
    error_i(err);
  }
};



// COMMAND: Tension, FEAT: tension

void wrapperGet_Tension() { 
  Serial.println(get_Tension()); 
}; 



