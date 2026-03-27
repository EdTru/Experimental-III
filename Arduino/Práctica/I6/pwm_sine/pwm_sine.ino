// ============================================================
//  PWM Sine Wave Generator
//  Single PWM pin (pin 9) + external RC low-pass filter
//  Type a frequency (Hz) in Serial Monitor to change it
//
//  Hardware needed:
//    Pin 9 --> R (10kΩ) --> output node --> capacitor (100nF) --> GND
//    Measure analog voltage at the output node
// ============================================================

// --- PWM pin (must be a PWM-capable pin: 3,5,6,9,10,11 on Uno) ---
const int PWM_PIN = 9;

// --- Sine table: 256 samples, 8-bit resolution (0-255) ---
// Values = round(127.5 + 127.5 * sin(2*pi*i/256))
const uint8_t sineTable[256] = {
  128,131,134,137,140,143,146,149,152,155,158,162,165,168,171,174,
  176,179,182,185,188,191,193,196,199,201,204,206,209,211,213,216,
  218,220,222,224,226,228,230,232,234,235,237,238,240,241,243,244,
  245,246,248,249,250,250,251,252,253,253,254,254,254,255,255,255,
  255,255,255,255,254,254,254,253,253,252,251,250,250,249,248,246,
  245,244,243,241,240,238,237,235,234,232,230,228,226,224,222,220,
  218,216,213,211,209,206,204,201,199,196,193,191,188,185,182,179,
  176,174,171,168,165,162,158,155,152,149,146,143,140,137,134,131,
  128,124,121,118,115,112,109,106,103,100, 97, 93, 90, 87, 84, 81,
   79, 76, 73, 70, 67, 64, 62, 59, 56, 54, 51, 49, 46, 44, 42, 39,
   37, 35, 33, 31, 29, 27, 25, 23, 21, 20, 18, 17, 15, 14, 12, 11,
   10,  9,  7,  6,  5,  5,  4,  3,  2,  2,  1,  1,  1,  0,  0,  0,
    0,  0,  0,  0,  1,  1,  1,  2,  2,  3,  4,  5,  5,  6,  7,  9,
   10, 11, 12, 14, 15, 17, 18, 20, 21, 23, 25, 27, 29, 31, 33, 35,
   37, 39, 42, 44, 46, 49, 51, 54, 56, 59, 62, 64, 67, 70, 73, 76,
   79, 81, 84, 87, 90, 93, 97,100,103,106,109,112,115,118,121,124
};

// --- State ---
float   frequency    = 1.0;   // Hz
long    stepDelay_us = 0;     // microseconds between samples
int     sampleIndex  = 0;
bool    running      = true;

void setup() {
  Serial.begin(9600);
  pinMode(PWM_PIN, OUTPUT);

  // Set Timer1 (pin 9 & 10) to fast PWM, no prescaler → ~31.4 kHz
  // This pushes the PWM carrier far above the audio range so the RC
  // filter removes it easily without affecting the sine waveform.
  TCCR1A = _BV(COM1A1) | _BV(WGM10);  // Fast PWM 8-bit, non-inverting on OC1A
  TCCR1B = _BV(WGM12)  | _BV(CS10);   // No prescaler → f_PWM = 16MHz/256 ≈ 62.5 kHz

  setFrequency(frequency);
  printWelcome();
}

void loop() {
  // --- Check Serial for new frequency ---
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.equalsIgnoreCase("stop")) {
      running = false;
      analogWrite(PWM_PIN, 128);  // Output midpoint (DC ~2.5V)
      Serial.println(">> Signal stopped. Output set to 2.5V (midpoint).");
      return;
    }

    float newFreq = input.toFloat();
    if (newFreq > 0) {
      setFrequency(newFreq);
    } else {
      Serial.println("ERROR: Enter a positive number in Hz (e.g. 5) or 'stop'.");
    }
  }

  // --- Output next sine sample via PWM ---
  if (running) {
    OCR1A = sineTable[sampleIndex];           // Write directly to PWM register (faster than analogWrite)
    sampleIndex = (sampleIndex + 1) & 0xFF;   // Wrap at 256
    delayMicroseconds(stepDelay_us);
  }
}

// ---- Set frequency and recompute step delay ----
void setFrequency(float freq) {
  frequency    = freq;
  // 256 samples per cycle → delay per step = period / 256
  stepDelay_us = (long)((1000000.0 / freq) / 256.0);
  running      = true;
  sampleIndex  = 0;

  Serial.println("----------------------------------------");
  Serial.print("Frequency : ");
  Serial.print(frequency, 3);
  Serial.println(" Hz");
  Serial.print("Step delay: ");
  Serial.print(stepDelay_us);
  Serial.println(" us");
  Serial.println("----------------------------------------");
}

void printWelcome() {
  Serial.println("========================================");
  Serial.println("  PWM Sine Wave Generator");
  Serial.println("========================================");
  Serial.print("PWM pin   : "); Serial.println(PWM_PIN);
  Serial.println("PWM freq  : ~62.5 kHz (Timer1 fast PWM)");
  Serial.println("Samples   : 256 per cycle");
  Serial.println();
  Serial.println("RC filter (required on output):");
  Serial.println("  R = 10 kOhm, C = 100 nF");
  Serial.println("  Cutoff: ~160 Hz");
  Serial.println("  Best sine freq range: 0.1 - 20 Hz");
  Serial.println();
  Serial.println("Commands:");
  Serial.println("  <number>  Set frequency in Hz");
  Serial.println("  stop      Pause (output = 2.5V DC)");
  Serial.println("========================================");
}
