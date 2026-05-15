// ============================================================
//  NERVMACHER v1.0
//  Projekt: Versteckter Störsender mit zufälligen Geräuschen
//  Hardware: Arduino Nano / Micro / Uno
//  Autor: Manus AI
//  Datum: 2026-05-14
//
//  Beschreibung:
//  Spielt in zufälligen Intervallen (2–15 Minuten) eines von
//  mehreren nervigen Geräuschen ab:
//    - Grillenzirpen (naturgetreu mit PWM)
//    - Hochfrequentes Piepen (sehr laut, ~4 kHz)
//    - Doppelpiepen (kurz, schrill)
//    - Vibration (via Vibrationsmotor an separatem Pin)
//
//  Schaltung:
//    - Piezo-Buzzer (passiv) zwischen PIN_BUZZER und GND
//      (über NPN-Transistor BC547 für maximale Lautstärke)
//    - Vibrationsmotor zwischen PIN_VIBRO und GND
//      (über NPN-Transistor BC547)
//    - Status-LED (optional) an PIN_LED
// ============================================================

// ---- Pin-Definitionen ----
#define PIN_BUZZER   9    // PWM-fähiger Pin für Piezo (via Transistor)
#define PIN_VIBRO    7    // Vibrationsmotor (via Transistor)
#define PIN_LED      13   // Onboard-LED (optional, für Debug)

// ---- Zeitintervalle (in Millisekunden) ----
#define INTERVALL_MIN  120000UL   // Minimum: 2 Minuten
#define INTERVALL_MAX  900000UL   // Maximum: 15 Minuten

// ---- Grillenzirpen: Frequenz- und Timing-Parameter ----
// Echte Grillen: ~5 kHz Hauptfrequenz, 125 Pulse pro Burst,
// 5 Bursts pro Gruppe, 3–4 Gruppen, dann lange Pause
#define CRICKET_FREQ_BASE   4800  // Grundfrequenz in Hz
#define CRICKET_PULSE_US    104   // Halbe Periode bei ~4,8 kHz (µs)
#define CRICKET_PULSES      120   // Pulse pro Einzelzirpen
#define CRICKET_BURST_PAUSE  22   // Pause zwischen Bursts (ms)
#define CRICKET_BURSTS       5    // Bursts pro Gruppe
#define CRICKET_GROUP_PAUSE 180   // Pause zwischen Gruppen (ms)
#define CRICKET_GROUPS       4    // Gruppen pro Sequenz

// ---- Globale Variablen ----
unsigned long naechsterTon = 0;   // Zeitstempel für nächsten Ton

// ============================================================
//  SETUP
// ============================================================
void setup() {
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_VIBRO,  OUTPUT);
  pinMode(PIN_LED,    OUTPUT);

  // Zufallsgenerator mit offenem Analogpin initialisieren
  randomSeed(analogRead(A0));

  // Beim Start kurz blinken (zeigt an: Gerät ist aktiv)
  for (int i = 0; i < 3; i++) {
    digitalWrite(PIN_LED, HIGH);
    delay(100);
    digitalWrite(PIN_LED, LOW);
    delay(100);
  }

  // Ersten Zeitpunkt setzen (sofort beim Start: 3–8 Sekunden)
  // Damit kann man beim Einschalten prüfen, ob alles funktioniert
  naechsterTon = millis() + random(3000, 8000);
}

// ============================================================
//  HAUPTSCHLEIFE
// ============================================================
void loop() {
  if (millis() >= naechsterTon) {

    // Zufällig einen von 4 Sounds wählen
    int soundWahl = random(0, 4);

    switch (soundWahl) {
      case 0:
        spieleGrille();
        break;
      case 1:
        spieleHochtonPiepen();
        break;
      case 2:
        spieleDoppelPiepen();
        break;
      case 3:
        spieleVibration();
        break;
    }

    // Nächsten Zeitpunkt zufällig festlegen
    unsigned long wartezeit = random(INTERVALL_MIN, INTERVALL_MAX);
    naechsterTon = millis() + wartezeit;
  }
}

// ============================================================
//  SOUND 1: Grillenzirpen (naturgetreu)
//  Erzeugt mehrere Gruppen von Burst-Sequenzen wie eine echte
//  Grille. Die Frequenz steigt leicht innerhalb jedes Bursts.
// ============================================================
void spieleGrille() {
  int anzahlGruppen = random(2, CRICKET_GROUPS + 1);

  for (int g = 0; g < anzahlGruppen; g++) {
    int anzahlBursts = random(3, CRICKET_BURSTS + 1);

    for (int b = 0; b < anzahlBursts; b++) {
      // Einzelner Burst: 120 Pulse mit leicht steigender Frequenz
      int verzoegerung = CRICKET_PULSE_US;

      for (int p = 0; p < CRICKET_PULSES; p++) {
        digitalWrite(PIN_BUZZER, HIGH);
        delayMicroseconds(verzoegerung);
        digitalWrite(PIN_BUZZER, LOW);
        delayMicroseconds(verzoegerung);

        // Frequenz leicht erhöhen (Periode verkürzen) alle 12 Pulse
        if ((p % 12) == 0 && verzoegerung > 80) {
          verzoegerung--;
        }
      }

      // Kurze Pause zwischen Bursts
      delay(CRICKET_BURST_PAUSE + random(-5, 5));
    }

    // Längere Pause zwischen Gruppen
    delay(CRICKET_GROUP_PAUSE + random(-30, 30));
  }
}

// ============================================================
//  SOUND 2: Hochton-Piepen (sehr laut, schrill)
//  Einzelner langer Piepton bei ~4 kHz – maximal nervig
// ============================================================
void spieleHochtonPiepen() {
  // Drei kurze Pieptöne mit steigender Frequenz
  tone(PIN_BUZZER, 3800, 150);
  delay(200);
  tone(PIN_BUZZER, 4200, 150);
  delay(200);
  tone(PIN_BUZZER, 4700, 300);
  delay(350);
  noTone(PIN_BUZZER);
}

// ============================================================
//  SOUND 3: Doppelpiepen (kurz und schrill)
//  Zwei schnelle Pieptöne – klingt wie ein Rauchmelder-Alarm
// ============================================================
void spieleDoppelPiepen() {
  int wiederholungen = random(2, 5);

  for (int i = 0; i < wiederholungen; i++) {
    tone(PIN_BUZZER, 4000, 80);
    delay(100);
    tone(PIN_BUZZER, 4000, 80);
    delay(300);
  }
  noTone(PIN_BUZZER);
}

// ============================================================
//  SOUND 4: Vibration
//  Kurze Vibrationssequenz über den Vibrationsmotor
// ============================================================
void spieleVibration() {
  // Kurzes Summen + Vibration gleichzeitig
  int muster[] = {200, 100, 200, 100, 400};
  int pausen[]  = {150, 150, 150, 150, 0};

  for (int i = 0; i < 5; i++) {
    digitalWrite(PIN_VIBRO, HIGH);
    tone(PIN_BUZZER, 200, muster[i]);  // Tiefes Summen
    delay(muster[i]);
    digitalWrite(PIN_VIBRO, LOW);
    noTone(PIN_BUZZER);
    if (pausen[i] > 0) delay(pausen[i]);
  }
}
