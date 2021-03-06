//// ****** THIS FILE IS AUTOGENERATED ******
////
////          >>>> DO NOT CHANGE <<<<
////
/// 
///  Filename; C:\Users\Publico.LABORATORIOS\Desktop\instrumentacion y control\arduino lantz\lantz_servo.py
///  Source class: Servo
///  Generation timestamp: 2019-06-12T05:17:56.332396
///  Class code hash: ffca21f7b3cfb288e87f2bb172d571306d3676f6
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


  // angulo
  // <F> float as string 

  // Getter:
  //   Angulo? 
  // Returns: <F> 
  sCmd.addCommand("Angulo?", wrapperGet_Angulo); 

  // Setter:
  //   Angulo <F> 
  // Returns: OK or ERROR    
  sCmd.addCommand("Angulo", wrapperSet_Angulo); 

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
}

//// Code 

void getInfo() {
  Serial.print("Servo,");
  Serial.println(COMPILE_DATE_TIME);
}

void unrecognized(const char *command) {
  error("Unknown command");
}
//// Auto generated Feat and DictFeat Code
// COMMAND: Angulo, FEAT: angulo

void wrapperGet_Angulo() { 
  Serial.println(get_Angulo()); 
}; 


void wrapperSet_Angulo() {
  char *arg;
  
  arg = sCmd.next();
  if (arg == NULL) {
    error("No value stated");
    return;
  }
  float value = atof(arg);

  int err = set_Angulo(value);
  if (err == 0) {
    ok();
  } else {
    error_i(err);
  }
};



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



