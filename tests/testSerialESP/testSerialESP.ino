// Declaration and initialization of the input pin
int Analog_input = A0; // X-axis-signal
void setup ()
{
 pinMode (Analog_input, INPUT);
 Serial.begin (9600); // Serielle output with 9600 bps
}
// The program reads the current value of the input pins
// and output it via serial out
void loop ()
{
 float Analog;
 int Digital;

 // Current value will be read and converted to the voltage
 Analog = analogRead (Analog_input);

 // and outputted here
 //Serial.print ("Analog voltage value:"); Serial.print (Analog, 4); Serial.println ("V");
 
 if(Analog >= 555){
   Serial.println("Puerta abierta");
 }
 else if((300<=Analog) && (Analog<555)){
   Serial.println("Puerta cerrada");
 }
 else{
   Serial.println("???");
 }
 
 delay (1000);
}
