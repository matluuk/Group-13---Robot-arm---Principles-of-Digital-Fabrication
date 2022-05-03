
#include <PCA9685.h>

#define NSERVOS 6
// 110 70 40
// 80
const int SERVO_SIGN[NSERVOS] { 1, 1, -1, -1, 1, 1 };

PCA9685 pwmController;
PCA9685_ServoEval servo;

uint16_t pwms[NSERVOS];

void setup() {
  Serial.begin(9600);
  Wire.begin();

  pwmController.resetDevices();
  pwmController.init();
  pwmController.setPWMFreqServo();
    
  for (int i=0; i<NSERVOS; i++) {
    pwms[i] = servo.pwmForAngle(0);
  }

  pwmController.setChannelsPWM(0, NSERVOS, pwms);
}

void loop() {
  char buf[128];
  size_t r = Serial.readBytesUntil('\n', buf, 126);
  if (r) {
    buf[r] = ';';
    buf[r + 1] = 0;
  
    char nbuf[5];
    size_t npos = 0;
    
    for (int i=0; i<NSERVOS; i++) {
      npos += nextPart(&buf[npos], nbuf, ';');
      pwms[i] = servo.pwmForAngle(atoi(nbuf) * SERVO_SIGN[i]);
    }

    pwmController.setChannelsPWM(0, NSERVOS, pwms);
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
