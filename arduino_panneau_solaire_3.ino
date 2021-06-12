#include <servo.h> 
 
//IO Pins
int pinL = 1;              //Left Sensor IO Pin
int pinR = 2;              //Right Sensor IO Pin
int pinServo1 = 10;        //Servo 1 PWM pin
int pinU = 3;              //up Sensor IO Pin
int pinServo2 = 11;        //Servo 2 PWM pin
 
int leftValue = 0;         //The left Sensor Value
int rightValue = 0;        //The right Sensor Value
int upValue = 0;           //The left Sensor Value
int error1 =0;              //The Deviation between the 2 sensors
int errorAVG1 = 0;          //Error Average - Rolling 2 Point
int error2 =0;              //The Deviation between the 2 sensors
int errorAVG2 = 0;          //Error Average - Rolling 2 Point
 
 
Servo hServo1;              //The servo object
Servo hServo2;   
int Position = 45;         //Position to write out
 
int minPos = 7;            //Min Position
int maxPos = 160;          //Max Position
 
 
float output1 = (maxPos - minPos) /2;  //Initial output Position
float output2 = (maxPos - minPos) /2;  //Initial output Position
 
void setup()
{
 
Serial.begin(9600);  //9600
//pinMode(pinV, INPUT);
hServo1.attach(pinServo1);
hServo2.attach(pinServo2);
 
//Set Servo to Centre for Alignment Purpose
Serial.println("Moving Servo to start Position");
hServo1.write(output1);
hServo2.write(output2);
delay(2000);
Serial.println("Going Live................");
}
void loop()
{
  //Input Reading
   leftValue = analogRead(pinL);
   rightValue = analogRead(pinR);
   upValue = analogRead(pinU);
   error1 = leftValue - rightValue;
   error2 = -upValue + (leftValue+rightValue)/2;
   errorAVG1 = (errorAVG1 + error1) / 2;
   errorAVG2 = (errorAVG2 + error2) / 2;
  
 float newOutput1 = output1 + getTravel(errorAVG1);
 if (newOutput1 > maxPos)
 {
   newOutput1 = maxPos;
 }
 else
 { 
   if (newOutput1 < minPos)
   {
     newOutput1 = minPos;
   }
 }
    hServo1.write(newOutput1);
    output1 = newOutput1;
     
 float newOutput2 = output2 + getTravel(errorAVG2); 
 if (newOutput2 > maxPos)
 {
   newOutput2 = maxPos;
 }
 else
 { 
   if (newOutput2 < minPos)
   {
     newOutput2 = minPos;
   }
 }
    hServo2.write(newOutput2);
    output2 = newOutput2;
}
 
int getTravel(float errorAVG)
{
  int deadband = 50;         //Range for which to do nothing with output 10 = -10 to +10  
  // -1 = Left; +1 = Right
  
 if (errorAVG < (deadband * -1))
 {
   return -1;
 }
 else
 {
   if (errorAVG > deadband)
   {
     return 1;
   }
   else
   {
     return 0;
   }
 }
}
