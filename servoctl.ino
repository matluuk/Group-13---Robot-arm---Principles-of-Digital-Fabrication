#include <Servo.h>

#define NSERVOS 4

const int SERVO_PINS[NSERVOS] {6, 9, 10, 11};

Servo servos[NSERVOS];

void setup() {
  for (int i=0; i<NSERVOS; i++) {
    servos[i].attach(SERVO_PINS[i]);
  }
  Serial.begin(9600);
}

void loop() {
  char buf[128];
  size_t r = Serial.readBytesUntil('\n', buf, 126);
  if (r) {
    buf[r] = ';';
    buf[r + 1] = 0;
  
    char nbuf[4];
    size_t npos = 0;
    
    for (int i=0; i<NSERVOS; i++) {
      npos += nextPart(&buf[npos], nbuf, ';');
      servos[i].write(atoi(nbuf));
    }
  }
}

/**
 * Read the next part in a sequence of strings with a delimiter
 * 
 * @param string The sequence beginning at the next part, as a null-terminated string
 * @param buf The buffer to which the part is written. Must have space for a null-terminator.
 * @param delimiter The delimiter of the sequence
 * @return The number of bytes read, including the delimiter but excluding the null-terminator (unless it is the delimiter)
 */
size_t nextPart(const char *string, char *buf, char delimiter) {
  size_t i = 0;
  while (string[i] != delimiter && string[i] != 0) {
    buf[i] = string[i];
    i++;
  }
  buf[i] = 0;
  return string[i] == delimiter ? i + 1 : i;
}
