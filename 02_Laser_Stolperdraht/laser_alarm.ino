// ============================================================
//  LASER-STOLPERDRAHT-ALARM v1.0
//  Projekt: Unsichtbarer Laser-Bewegungsmelder mit Alarm
//  Hardware: Arduino Nano / Micro / Uno
//  Autor: Manus AI
//  Datum: 2026-05-15
//
//  Beschreibung:
//  Ein KY-008 Lasermodul sendet einen kontinuierlichen Strahl
//  auf einen LDR-Fotowiderstand. Wird der Strahl unterbrochen,
//  löst der Alarm aus:
//    - Piezo-Buzzer spielt eine Alarmsirene (auf/ab Sweep)
//    - Rote LED blinkt schnell
//    - Grüne Status-LED zeigt "Scharf" an
//    - Serieller Monitor zeigt Zeitstempel der Auslösung
//
//  Modi:
//    - SCHARF:    Laser aktiv, LDR überwacht, Alarm bereit
//    - ALARM:     Strahl unterbrochen, Sirene + LED aktiv
//    - STUMM:     Taster gedrückt, Alarm wird zurückgesetzt
//
//  Schaltung:
//    - KY-008 Laser:  S-Pin → PIN_LASER, GND → GND, + → 5V
//    - LDR:           Spannungsteiler mit 10kΩ → PIN_LDR (A0)
//    - Piezo (passiv): PIN_BUZZER → Buzzer → GND
//    - Rote LED:      PIN_LED_ROT → 220Ω → LED → GND
//    - Grüne LED:     PIN_LED_GRUEN → 220Ω → LED → GND
//    - Reset-Taster:  PIN_TASTER → Taster → GND (INPUT_PULLUP)
// ============================================================

// ---- Pin-Definitionen ----
#define PIN_LASER       7    // KY-008 Laser-Signal
#define PIN_LDR         A0   // LDR Fotowiderstand (Analogeingang)
#define PIN_BUZZER      9    // PWM-Pin für Piezo-Buzzer
#define PIN_LED_ROT     6    // Rote Alarm-LED
#define PIN_LED_GRUEN   5    // Grüne Status-LED ("Scharf")
#define PIN_TASTER      2    // Reset/Stumm-Taster (mit Pull-Up)

// ---- Kalibrierung ----
// Beim Start wird der Helligkeitswert des Lasers gemessen.
// SCHWELLWERT_PROZENT gibt an, wie weit der Wert abfallen muss,
// damit ein Alarm ausgelöst wird (z.B. 40% = 40% unter Basiswert).
#define SCHWELLWERT_PROZENT  40   // Empfindlichkeit: 20–60 empfohlen
#define KALIBRIERUNGS_DAUER  3000 // Kalibrierungszeit in ms beim Start

// ---- Alarm-Töne ----
#define SIRENE_FREQ_MIN  800   // Unterste Frequenz der Sirene (Hz)
#define SIRENE_FREQ_MAX  2400  // Oberste Frequenz der Sirene (Hz)
#define SIRENE_SCHRITT   30    // Frequenzschritte der Sirene

// ---- Globale Variablen ----
int    basiswert       = 0;    // Kalibrierter LDR-Wert mit Laser
int    schwellwert     = 0;    // Berechneter Auslöseschwellwert
bool   alarmAktiv      = false;
bool   systemScharf    = false;
unsigned long alarmZeit = 0;

// Für nicht-blockierende Sirene
int    sireneFreq      = SIRENE_FREQ_MIN;
int    sireneRichtung  = 1;    // +1 = aufsteigend, -1 = absteigend
unsigned long letzterSireneTon = 0;

// Für nicht-blockierendes LED-Blinken
bool   ledZustand      = false;
unsigned long letztesLedBlinken = 0;

// ============================================================
//  SETUP
// ============================================================
void setup() {
  Serial.begin(9600);
  Serial.println(F("===================================="));
  Serial.println(F("  LASER-STOLPERDRAHT-ALARM v1.0"));
  Serial.println(F("===================================="));

  // Pins konfigurieren
  pinMode(PIN_LASER,     OUTPUT);
  pinMode(PIN_BUZZER,    OUTPUT);
  pinMode(PIN_LED_ROT,   OUTPUT);
  pinMode(PIN_LED_GRUEN, OUTPUT);
  pinMode(PIN_TASTER,    INPUT_PULLUP);  // Interner Pull-Up

  // Laser einschalten
  digitalWrite(PIN_LASER, HIGH);
  delay(500);  // Laser stabilisieren lassen

  // ---- Kalibrierung ----
  Serial.println(F("Kalibrierung laeuft... Laser auf LDR richten!"));
  kalibriere();

  // System scharf schalten
  systemScharf = true;
  digitalWrite(PIN_LED_GRUEN, HIGH);
  Serial.println(F("System SCHARF. Alarm bereit."));
  Serial.print(F("Basiswert: "));
  Serial.print(basiswert);
  Serial.print(F("  |  Schwellwert: "));
  Serial.println(schwellwert);
}

// ============================================================
//  HAUPTSCHLEIFE
// ============================================================
void loop() {
  // Taster prüfen (Alarm zurücksetzen)
  if (digitalRead(PIN_TASTER) == LOW) {
    alarmZuruecksetzen();
    delay(300);  // Entprellung
    return;
  }

  if (!systemScharf) return;

  // LDR-Wert lesen
  int ldrWert = analogRead(PIN_LDR);

  // Alarm auslösen, wenn Strahl unterbrochen
  if (!alarmAktiv && ldrWert < schwellwert) {
    alarmAuslösen(ldrWert);
  }

  // Alarm-Effekte (nicht-blockierend)
  if (alarmAktiv) {
    sireneAbspielen();
    ledBlinken();
  }
}

// ============================================================
//  KALIBRIERUNG
//  Misst den Durchschnittswert des LDR mit aktivem Laser
//  und berechnet den Auslöseschwellwert.
// ============================================================
void kalibriere() {
  // Grüne LED blinkt während der Kalibrierung
  long summe = 0;
  int  messungen = 0;
  unsigned long startzeit = millis();

  while (millis() - startzeit < KALIBRIERUNGS_DAUER) {
    summe += analogRead(PIN_LDR);
    messungen++;
    digitalWrite(PIN_LED_GRUEN, (millis() / 200) % 2);  // Blinken
    delay(10);
  }

  basiswert   = summe / messungen;
  schwellwert = basiswert - (basiswert * SCHWELLWERT_PROZENT / 100);

  // Kurzes Bestätigungssignal
  digitalWrite(PIN_LED_GRUEN, LOW);
  for (int i = 0; i < 3; i++) {
    tone(PIN_BUZZER, 1200, 80);
    delay(150);
  }
  noTone(PIN_BUZZER);
}

// ============================================================
//  ALARM AUSLÖSEN
// ============================================================
void alarmAuslösen(int gemessenerWert) {
  alarmAktiv  = true;
  alarmZeit   = millis();
  sireneFreq  = SIRENE_FREQ_MIN;
  sireneRichtung = 1;

  // Grüne LED aus, rote LED an
  digitalWrite(PIN_LED_GRUEN, LOW);

  Serial.println(F(""));
  Serial.println(F("!!! ALARM !!! STRAHL UNTERBROCHEN !!!"));
  Serial.print(F("Zeitstempel (ms seit Start): "));
  Serial.println(alarmZeit);
  Serial.print(F("Gemessener LDR-Wert: "));
  Serial.print(gemessenerWert);
  Serial.print(F("  |  Schwellwert war: "));
  Serial.println(schwellwert);
  Serial.println(F("Taster druecken zum Zuruecksetzen."));
}

// ============================================================
//  ALARM ZURÜCKSETZEN
// ============================================================
void alarmZuruecksetzen() {
  if (!alarmAktiv) return;

  alarmAktiv = false;
  noTone(PIN_BUZZER);
  digitalWrite(PIN_LED_ROT,   LOW);
  digitalWrite(PIN_LED_GRUEN, HIGH);

  Serial.println(F(""));
  Serial.println(F("Alarm zurueckgesetzt. System wieder SCHARF."));

  // Bestätigungston
  tone(PIN_BUZZER, 800, 100);
  delay(150);
  tone(PIN_BUZZER, 1200, 100);
  delay(150);
  noTone(PIN_BUZZER);
}

// ============================================================
//  SIRENE ABSPIELEN (nicht-blockierend)
//  Erzeugt einen auf- und absteigenden Frequenz-Sweep
// ============================================================
void sireneAbspielen() {
  unsigned long jetzt = millis();
  if (jetzt - letzterSireneTon < 8) return;  // Alle 8ms Schritt
  letzterSireneTon = jetzt;

  tone(PIN_BUZZER, sireneFreq);

  sireneFreq += sireneRichtung * SIRENE_SCHRITT;

  if (sireneFreq >= SIRENE_FREQ_MAX) {
    sireneFreq     = SIRENE_FREQ_MAX;
    sireneRichtung = -1;
  } else if (sireneFreq <= SIRENE_FREQ_MIN) {
    sireneFreq     = SIRENE_FREQ_MIN;
    sireneRichtung = 1;
  }
}

// ============================================================
//  LED BLINKEN (nicht-blockierend)
// ============================================================
void ledBlinken() {
  unsigned long jetzt = millis();
  if (jetzt - letztesLedBlinken < 120) return;  // Alle 120ms umschalten
  letztesLedBlinken = jetzt;

  ledZustand = !ledZustand;
  digitalWrite(PIN_LED_ROT, ledZustand ? HIGH : LOW);
}
