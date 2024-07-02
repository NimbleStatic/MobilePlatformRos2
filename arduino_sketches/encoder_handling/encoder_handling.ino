int R_H1_PIN = 2; int R_H2_PIN = 4;
bool R_dir; long int R_abs_pos; int R_pos_change;
byte R_last_h1;

int L_H1_PIN = 3; int L_H2_PIN = 5;
bool L_dir; long int L_abs_pos; int L_pos_change;
byte L_last_h1;

long int Tp = 100000;
int nr_to_full_revolve = 300;

void encoder_setup(){

  

  pinMode(R_H1_PIN, INPUT); pinMode(R_H2_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(R_H1_PIN), r_mot_interrupt, CHANGE);
  R_dir = true;
  R_last_h1 = digitalRead(R_H1_PIN);
  R_abs_pos = 0;
  R_pos_change = 0;

  pinMode(L_H1_PIN, INPUT); pinMode(L_H2_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(L_H1_PIN), l_mot_interrupt, CHANGE);
  L_dir = true;
  L_last_h1 = digitalRead(L_H1_PIN);
  L_abs_pos = 0;
  L_pos_change = 0;
}



void run_for_n_microseconds(long int n, void (*func)(void)){
  long int s_time = micros();
  long int time_to_end = s_time + n -4;
  func();
  bool flag = true;
  long int t;
  while (flag){
    t = micros();
    if ((t >= time_to_end) || (t < s_time)){
      flag = false;
    }
  }
};

void r_mot_interrupt(){
  int h1 = digitalRead(R_H1_PIN);
  if ((R_last_h1 == 0) && (h1 == 1)){
    int h2 = digitalRead(R_H2_PIN);
    if (h2 == 0 && R_dir){
      R_dir = false;
    } else if (h2 == 1 && !R_dir){
      R_dir = true;
    }
  }

  R_last_h1 = h1;
  if (!R_dir){R_abs_pos ++;} else {R_abs_pos --;}
}

void l_mot_interrupt(){
  int h1 = digitalRead(L_H1_PIN);
  if ((L_last_h1 == 0) && (h1 == 1)){
    int h2 = digitalRead(L_H2_PIN);
    if (h2 == 0 && L_dir){
      L_dir = false;
    } else if (h2 == 1 && !L_dir){
      L_dir = true;
    }
  }

  L_last_h1 = h1;
  if (!L_dir){L_abs_pos ++;} else {L_abs_pos --;}
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  encoder_setup();

}

void print_abs_pos(){
  String message;
  message += "R:" + String(R_abs_pos);
  message += " L:" + String(L_abs_pos);
  Serial.print(message);
  Serial.print(" Time:");
  Serial.println(micros());
  }

void loop() {
  // put your main code here, to run repeatedly:
  run_for_n_microseconds((Tp), print_abs_pos);

}
