// Declaration and initialization of the input pin
int Analog_input = A0; // X-axis-signal
void setup ()
{
  pinMode(Analog_input, INPUT);
  Serial.begin (9600); // Serielle output with 9600 bps
}
// The program reads the current value of the input pins
// and output it via serial out
void loop ()
{
  int Analog;
  int Digital;

  // Current value will be read and converted to the voltage
  char buffer[50];
  Analog = analogRead(Analog_input);
  sprintf(buffer, "%d", Analog);
  Serial.println(buffer);

  //Serial.write(String(Analog));
  //Serial.print("x");

  delay (1000);
}
