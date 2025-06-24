import java.util.*;
import com.hamoid.*;

String[] monthNames = {"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"};

int DAY_LEN;
int PEOPLE_COUNT;
String[] textFile;
Person[] people;
int TOP_VISIBLE = 10;
float[] maxes;
int[] unitChoices;

float X_MIN = 100;
float X_MAX = 1900;
float Y_MIN = 300;
float Y_MAX = 1000;
float X_W = X_MAX-X_MIN;
float Y_H = Y_MAX-Y_MIN;
float BAR_PROPORTION = 0.9;
int START_DATE = dateToDays("2021-01-01");
float TEXT_MARGIN = 8;

float currentScale = -1;

int frames = 0;
float currentDay = 0;
float FRAMES_PER_DAY = 5;
float BAR_HEIGHT;
PFont font;

int[] unitPresets = {1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000};
VideoExport videoExport;

void setup(){
  font = loadFont("Jygquif1-96.vlw");
  randomSeed(432766);
  textFile = loadStrings("data.tsv");
  String[] parts = textFile[0].split("\t");
  DAY_LEN = textFile.length-1;
  PEOPLE_COUNT = parts.length-1;
  
  maxes = new float[DAY_LEN];
  unitChoices = new int[DAY_LEN];
  for(int d = 0; d < DAY_LEN; d++){
    maxes[d] = 0;
  }
  
  people = new Person[PEOPLE_COUNT];
  for(int i = 0; i < PEOPLE_COUNT; i++){
    people[i] = new Person(parts[i+1]);
  }
  for(int d = 0; d < DAY_LEN; d++){
    String[] dataParts = textFile[d+1].split("\t");
    for(int p = 0; p < PEOPLE_COUNT; p++){
      float val = Float.parseFloat(dataParts[p+1]);
      people[p].values[d] = val;
      if(val > maxes[d]){
        maxes[d] = val;
      }
    }
  }
  getRankings();
  getUnits();
  for(int d = 0; d < DAY_LEN; d++){
    println(unitChoices[d]);
  }
  BAR_HEIGHT = (rankToY(1)-rankToY(0))*BAR_PROPORTION;
  size(1920,1080);
  
  videoExport = new VideoExport(this,"VideoTeste.mp4");
  videoExport.startMovie();
}

int START_DAY = 0;
void draw(){
  currentDay = getDayFromFrameCount(frames);
  currentScale = getXScale(currentDay);
  drawBackground();
  drawHorizTickmarks();
  drawBars();

  //saveImage();
  videoExport.saveFrame();
  if(getDayFromFrameCount(frames+1) >= DAY_LEN){
    videoExport.endMovie();
    exit();
  }
  frames++;
}

void saveImage(){
  saveFrame("tutorialImages/img"+frames+".png");
}

float getDayFromFrameCount(int fc){
  return fc/FRAMES_PER_DAY+START_DAY;
}

void drawBackground(){
  background(0);
  fill(255);
  textFont(font,144);
  textAlign(RIGHT);
  text(daysToDate(currentDay,true),width-40,150);
  fill(100);
  textAlign(CENTER);
  textFont(font,62);
  text("Tempos",840,Y_MIN-100);
}

void drawHorizTickmarks(){
  float preferredUnit = WAIndex(unitChoices, currentDay, 4);
  float unitRem = preferredUnit%1.0;
  if(unitRem < 0.001){
    unitRem = 0;
  }else if(unitRem >= 0.999){
    unitRem = 0;
    preferredUnit = ceil(preferredUnit);
  }
  int thisUnit = unitPresets[(int)preferredUnit];
  int nextUnit = unitPresets[(int)preferredUnit+1];
  
  drawTickMarksOfUnit(thisUnit,255-unitRem*255);
  if(unitRem >= 0.001){
    drawTickMarksOfUnit(nextUnit,unitRem*255);
  }
}

void drawTickMarksOfUnit(int u, float alpha){
  for(int v = 0; v < currentScale*1.4; v+=u){
    float x = valueToX(v);
    fill(100,100,100,alpha);
    float W = 4;
    rect(x-W/2,Y_MIN-20,W,Y_H+20);
    textAlign(CENTER);
    textFont(font,62);
    text(keyify(v),x,Y_MIN-30);
  }
}

void drawBars(){
  noStroke();
  for(int p = 0; p < PEOPLE_COUNT; p++){
    Person pe = people[p];
    float val = linIndex(pe.values,currentDay);
    
    // Só mostra se o valor for maior que 0
    if(val > 0) {
      float x = valueToX(val);
      float rank = WAIndex(pe.ranks, currentDay, 0.5);
      float y = rankToY(rank);
      
      // Desenha a barra
      fill(pe.c);
      rect(X_MIN,y,x-X_MIN,BAR_HEIGHT);
      
      // Configurações de texto
      fill(255);
      textFont(font,52);
      
      // Nome do jogador alinhado à esquerda
      textAlign(LEFT, CENTER);
      text(pe.name, X_MIN + 15, y + BAR_HEIGHT/2);
      
      // Tempo do jogador colado ao final da barra (com margem)
      textAlign(LEFT, CENTER);
      float textX = max(X_MIN + 15, x + 10);
      text(formatTime(val), textX, y + BAR_HEIGHT/2);
    }
  }
}

void getRankings(){
  for(int d = 0; d < DAY_LEN; d++){
    boolean[] taken = new boolean[PEOPLE_COUNT];
    for(int p = 0; p < PEOPLE_COUNT; p++){
      taken[p] = false;
    }
    for(int spot = 0; spot < TOP_VISIBLE; spot++){
      float record = -1;
      int holder = -1;
      for(int p = 0; p < PEOPLE_COUNT; p++){
        if(!taken[p]){
          float val = people[p].values[d];
          if(val > record){
            record = val;
            holder = p;
          }
        }
      }
      people[holder].ranks[d] = spot;
      taken[holder] = true;
    }
  }
}

float stepIndex(float[] a, float index){
  return a[(int)index];
}

float linIndex(float[] a, float index){
  int indexInt = (int)index;
  float indexRem = index%1.0;
  float beforeVal = a[indexInt];
  float afterVal = a[min(DAY_LEN-1,indexInt+1)];
  return lerp(beforeVal,afterVal,indexRem);
}

float WAIndex(float[] a, float index, float WINDOW_WIDTH){
  int startIndex = max(0,ceil(index-WINDOW_WIDTH));
  int endIndex = min(DAY_LEN-1,floor(index+WINDOW_WIDTH));
  float counter = 0;
  float summer = 0;
  for(int d = startIndex; d <= endIndex; d++){
    float val = a[d];
    float weight = 0.5+0.5*cos((d-index)/WINDOW_WIDTH*PI);
    counter += weight;
    summer += val*weight;
  }
  float finalResult = summer/counter;
  return finalResult;
}

float WAIndex(int[] a, float index, float WINDOW_WIDTH){
  float[] aFloat = new float[a.length];
  for(int i = 0; i < a.length; i++){
    aFloat[i] = a[i];
  }
  return WAIndex(aFloat,index,WINDOW_WIDTH);
}

float getXScale(float d){
  return WAIndex(maxes,d,14)*1.2;
}

float valueToX(float val){
  return X_MIN+X_W*val/currentScale;
}

float rankToY(float rank){
  float y = Y_MIN+rank*(Y_H/TOP_VISIBLE);
  return y;
}

String daysToDate(float daysF, boolean longForm){
  int days = (int)daysF+START_DATE+1;
  Date d1 = new Date();
  d1.setTime(days*86400000l);
  int year = d1.getYear()+1900;
  int month = d1.getMonth()+1;
  int date = d1.getDate();
  if(longForm){
    return year+" "+monthNames[month-1]+" "+date;
  }else{
    return year+"-"+nf(month,2,0)+"-"+nf(date,2,0);
  }
}

int dateToDays(String s){
  int year = Integer.parseInt(s.substring(0,4))-1900;
  int month = Integer.parseInt(s.substring(5,7))-1;
  int date = Integer.parseInt(s.substring(8,10));
  Date d1 = new Date(year, month, date, 6, 6, 6);
  int days = (int)(d1.getTime()/86400000L);
  return days;
}

void getUnits(){
  for(int d = 0; d < DAY_LEN; d++){
    float Xscale = getXScale(d);
    for(int u = 0; u < unitPresets.length; u++){
      if(unitPresets[u] >= Xscale/3.0){
        unitChoices[d] = u-1;
        break;
      }
    }
  }
}

String keyify(int n){
  return formatTime(n);
}

String formatTime(float seconds) {
  if(seconds <= 0) return ""; // Retorna string vazia para valores zero
  
  int s = (int) seconds;
  int h = s / 3600;
  s %= 3600;
  int m = s / 60;
  s %= 60;

  if (h > 0) {
    return nf(h, 2) + ":" + nf(m, 2) + ":" + nf(s, 2);
  } else if (m > 0) {
    return nf(m, 2) + ":" + nf(s, 2);
  } else if (s > 0) {
    return nf(s, 2);
  }
  return ""; // Caso todos sejam zero
}
