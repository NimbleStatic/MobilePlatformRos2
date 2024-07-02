#include <SPI.h>

void setup() {
  // have to send on master in, *slave out*
  Serial.begin(9600);
  pinMode(MISO, OUTPUT);

  // turn on SPI in slave mode
  SPCR |= _BV(SPE);

  // turn on interrupts
  SPI.attachInterrupt();
}

// SPI interrupt routine
ISR (SPI_STC_vect)
{
  byte c = SPDR;
  Serial.println(SPDR);
  if (SPDR == 0x01) {
    // Send data A to SPI master
    SPI.send(0x99);
  }else if (SPDR == 0x02) {
    // Send data A to SPI master
    SPI.send(0x98);}
//  if (c == 1){
//    SPDR = 99;
//  }
//  if (c == 2){
//    SPDR = 98;
//  }
//  if (c == 3){
//    SPDR = 97;
//  }
//  if (c == 4){
//    SPDR = 96;
//  }
//  
}  // end of interrupt service routine (ISR) for SPI

void loop () { }
