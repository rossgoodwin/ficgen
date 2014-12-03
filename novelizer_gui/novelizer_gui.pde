// FICTION GENERATOR BY ROSS GOODWIN
// http://rossgoodwin.com/ficgen

import java.io.*;


// paths and such
String sysPath = "/Users/rg/Projects/plotgen/ficgen/";
String novPath = "/Users/rg/Google Drive/novels/";
String rgPath = "/Users/rg/";
String novelTitle = "You Forgot To Write A Title";
String firstName = "John";
String lastName = "Doe";
String toEmail = "ross.goodwin@gmail.com";
boolean finished = false;
boolean generation = false;
boolean started = false;

// time to go!
int beepBeep;

// fonts
PFont gotham32;
PFont gotham18;
PFont gothamNarrow16;


// GUI Elements
PVector title;

PVector generateButton;
PShape generateSymbol;

void setup() {
  size(displayWidth, displayHeight);
  gotham32 = loadFont("Gotham-Book-32.vlw");
  gotham18 = loadFont("Gotham-Book-18.vlw");
  gothamNarrow16 = loadFont("GothamXNarrow-Thin-16.vlw");
  
  title = new PVector(width/2, 50);
  
  generateButton = new PVector(width/2, height-100);
  generateSymbol = loadShape("generate_symbol.svg");
  
}

void draw() {
  // set values equal to userText variables
  if (titleInput.filled && !titleInput.userText.equals("")) novelTitle = titleInput.userText;
  if (firstNameInput.filled && !firstNameInput.userText.equals("")) firstName = firstNameInput.userText;
  if (surnameInput.filled && !surnameInput.userText.equals("")) lastName = surnameInput.userText;
  if (emailInput.filled && !emailInput.userText.equals("")) toEmail = emailInput.userText;
  
  // background
  background(236, 240, 241);
  
  // headline and border
  textFont(gotham32);
  textAlign(CENTER, TOP);
  fill(108, 122, 137);
  noStroke();
  text("FICTION GENERATOR", title.x, title.y);
  
  // text input boxes
  titleInput.display();
  firstNameInput.display();
  surnameInput.display();
  emailInput.display();
  
  // genre buttons
  noFill();
  stroke(108, 122, 137);
  rectMode(CORNER);
  rect(40, 305, 80*6+10, 80*3+10);
  
  textFont(gothamNarrow16);
  textAlign(LEFT, BOTTOM);
  fill(108, 122, 137);
  noStroke();
  text("GENRES", 50, 305);
  
  for (int i=0; i<genreButtons.length; i++) {
    genreButtons[i].display();
  }
  
  // conflict buttons
  noFill();
  stroke(108, 122, 137);
  rectMode(CORNER);
  rect(40, 580, 80*5+10, 80*2+10);
  
  textFont(gothamNarrow16);
  textAlign(LEFT, BOTTOM);
  fill(108, 122, 137);
  noStroke();
  text("CONFLICT", 50, 580);
  
  for (int i=0; i<conflictButtons.length; i++) {
    conflictButtons[i].display();
  }
  
  // narrator buttons
  noFill();
  stroke(108, 122, 137);
  rectMode(CORNER);
  rect(narX-45, narY-45, 80*2+10, 80*3+10);
  
  textFont(gothamNarrow16);
  textAlign(LEFT, BOTTOM);
  fill(108, 122, 137);
  noStroke();
  text("NARRATOR", narX-35, narY-45);
  
  for (int i=0; i<narrButtons.length; i++) {
    narrButtons[i].display();
  }
  
  // sliders
  for (int i=0; i<sliders.length; i++) {
    if (sliders[i].active) sliders[i].boxPos.x = mouseX;
    if (sliders[i].active && mouseX < sliX) sliders[i].boxPos.x = sliX;
    if (sliders[i].active && mouseX > sliX+300) sliders[i].boxPos.x = sliX+300;
    sliders[i].display();
  }
  
  // generate button
  // noFill();
  // stroke(108, 122, 137);
  // rectMode(CENTER);
  // rect(generateButton.x, generateButton.y, 120, 120);
  
  noStroke();
  fill(231, 76, 60);
  rectMode(CENTER);
  rect(generateButton.x, generateButton.y, 100, 100);
  
  shapeMode(CENTER);
  fill(255);
  noStroke();
  shape(generateSymbol, generateButton.x, generateButton.y-3, 65, 65);
  
  if (started) {
    fill(0, 20);
    rectMode(CENTER);
    rect(generateButton.x, generateButton.y, 100, 100);
  } else {
    fill(0, 20);
    rectMode(CENTER);
    rect(generateButton.x, generateButton.y+45, 100, 10);
  }
  
  
  // GOOOOOO!!!
  if (generation && frameCount >= beepBeep) {
    generate();
    generation = false;
  }
  
}

void generate() {
  String[] genreArgArr = new String[genreButtons.length];
  for (int i=0; i<genreButtons.length; i++) {
    if (genreButtons[i].pressed) {
      genreArgArr[i] = genreButtons[i].label.toLowerCase();
    } else {
      genreArgArr[i] = "";
    }
  }
  String genreArgs = "";
  for (int i=0; i<genreArgArr.length; i++) {
    if (!genreArgArr[i].equals("")) {
      genreArgs += (genreArgArr[i]+" ");
    }
  }
  genreArgs = trim(genreArgs);
  String[] genreArgsList = split(genreArgs, " ");
  
  String[] conflictArgArr = new String[conflictButtons.length];
  for (int i=0; i<conflictButtons.length; i++) {
    if (conflictButtons[i].pressed) {
      conflictArgArr[i] = conflictButtons[i].label.toLowerCase();
    } else {
      conflictArgArr[i] = "";
    }
  }
  String conflictArgs = trim(join(conflictArgArr, " "));

  // String[] narrArgArr = new String[narrButtons.length];
  // for (int i=0; i<narrButtons.length; i++) {
  //   if (narrButtons[i].pressed) {
  //     narrArgArr[i] = narrButtons[i].label.toLowerCase();
  //   } else {
  //     narrArgArr[i] = "";
  //   }
  // }
  // String narrArgs = trim(join(narrArgArr, " "));
  
  // GENERATE NOVEL
  String[] paramsNovel = {
    "/usr/bin/python", sysPath+"ficgen.py",
    "--title", trim(novelTitle), "--charnames", trim(firstName)+"_"+trim(lastName), 
    "--genre", genreArgsList[0], genreArgsList[1], genreArgsList[2], 
    "--conflict", conflictArgs,
    "--passion", str(conSli(passionSlider.boxPos.x)), "--verbosity", str(conSli(verbositySlider.boxPos.x)),
    "--realism", str(conSli(realismSlider.boxPos.x)), "--length", str(conSli(lengthSlider.boxPos.x)),
    "--charcount", str(conSli(charCountSlider.boxPos.x)), "--density", str(conSli(densitySlider.boxPos.x)),
    "--accessibility", str(conSli(accessibilitySlider.boxPos.x)), "--depravity", str(conSli(depravitySlider.boxPos.x)),
    "--linearity", str(conSli(linearitySlider.boxPos.x))
  };
  
  
  
  try {
    // ProcessBuilder pb = new ProcessBuilder(paramsNovel);
    // pb.redirectErrorStream(true);
    
    // Process p = pb.start();
    // InputStreamReader isr = new InputStreamReader(p.getInputStream());
    // BufferedReader br = new BufferedReader(isr);
    
    // String lineRead;
    // while ((lineRead = br.readLine()) != null) {
    //   println(lineRead);
    // }
    Process p = exec(paramsNovel);
    
    int x = p.waitFor();
    println(x);
  }
  catch (Exception err) {
    err.printStackTrace();
  }
  
  // String novelParams = join(paramsNovel, " ");
  // println(novelParams);
  
  //String[] novelParameters = {};
  
  // try {
  //   Process p = exec(paramsNovel);
  //   int x = p.waitFor();
  //   println(x);
  //   println("NOVEL GENERATION SUCCESS");
  // }
  // catch (Exception err) {
  //   err.printStackTrace();
  //   println("NOVEL GENERATION FAILED");
  // }
  
  // println("WAITING...");
  // delay(30000);
  // println("WE GOT THERE!");
  
  // CONVERT TO PDF
  String novelFile = sysPath + "output/" + novelTitle + ".tex";
  String[] paramsPDF = {"/usr/texbin/pdflatex", "-interaction", "nonstopmode", novelFile};
  try {
    Process p0 = exec(paramsPDF);
    p0.waitFor();
    println("PDF CONVERSION SUCCESS");
  }
  catch (Exception err) {
    err.printStackTrace();
    println("PDF CONVERSION FAILED");
  }
  
  // filenames
  String pdfName = novelTitle + ".pdf";
  String auxName = novelTitle + ".aux";
  String logName = novelTitle + ".log";
  String outName = novelTitle + ".out";
  
  // take out the trash (remove log files)
  String[] paramsRm = {"rm", auxName, logName, outName};
  try {
    Process p1 = exec(paramsRm);
    p1.waitFor();
  }
  catch (Exception err) {
    err.printStackTrace();
  }
  
  // move the cargo (novelTitle.pdf goes to Google Drive/novels/)
  String[] paramsMv = {"cp", pdfName, novPath};
  try {
    Process p2 = exec(paramsMv);
    p2.waitFor();
  }
  catch (Exception err) {
    err.printStackTrace();
  }
  
  // send email
  String[] paramsSend = {"python", sysPath+"sendnovel.py", trim(toEmail), pdfName};
  try {
    Process p3 = exec(paramsSend);
    p3.waitFor();
  }
  catch (Exception err) {
    err.printStackTrace();
  }
  
  // speak
  String talk = "Thanks for the inspiration, " + firstName + ". I just wrote your story, and I think it's a real page turner. No spoilers though. You'll have to read it for yourself. I sent you the PDF. Enjoy!";
  String[] paramsSay = {"say", talk};
  exec(paramsSay);
  
  // open the PDF
  open(pdfName);
}

void mousePressed() {
  
  if (mouseX > generateButton.x-50 && mouseX < generateButton.x+50 && mouseY > generateButton.y-50 && mouseY < generateButton.y+50) {
  
    beepBeep = frameCount + int(frameRate*2);
    
    started = true;
    generation = true;
    
  }
  
  // input fields
  for (int i=0; i<inputFields.length; i++) {
    if (mouseX > inputFields[i].pos.x && mouseX < inputFields[i].pos.x+inputFields[i].widthHeight.x && mouseY > inputFields[i].pos.y && mouseY < inputFields[i].pos.y+inputFields[i].widthHeight.y) {
      inputFields[i].active = true;
      inputFields[i].filled = true;
    } else if (inputFields[i].userText.equals("")) {
      inputFields[i].active = false;
      inputFields[i].filled = false;
    } else {
      inputFields[i].active = false;
    }
  }
  
  // genre buttons
  for (int i=0; i<genreButtons.length; i++) {
    if (mouseX > genreButtons[i].pos.x-35 && mouseX < genreButtons[i].pos.x+35 && mouseY > genreButtons[i].pos.y-35 && mouseY < genreButtons[i].pos.y+35) {
      genreButtons[i].pressed = !genreButtons[i].pressed;
    }
  }
  
  // conflict buttons
  for (int i=0; i<conflictButtons.length; i++) {
    
    if (mouseX > conflictButtons[i].pos.x-35 && mouseX < conflictButtons[i].pos.x+35 && mouseY > conflictButtons[i].pos.y-35 && mouseY < conflictButtons[i].pos.y+35) {
      for (int j=0; j<conflictButtons.length; j++) {
        if (conflictButtons[j].pressed) conflictButtons[j].pressed = false;
      }
      conflictButtons[i].pressed = !conflictButtons[i].pressed;
    }
  
  }
  
  // narrator buttons
  for (int i=0; i<narrButtons.length; i++) {
    
    if (mouseX > narrButtons[i].pos.x-35 && mouseX < narrButtons[i].pos.x+35 && mouseY > narrButtons[i].pos.y-35 && mouseY < narrButtons[i].pos.y+35) {
      for (int j=0; j<narrButtons.length; j++) {
        if (narrButtons[j].pressed) narrButtons[j].pressed = false;
      }
      narrButtons[i].pressed = !narrButtons[i].pressed;
    }
  
  }
  
  // sliders
  for (int i=0; i<sliders.length; i++) {
    if (mouseX > sliders[i].boxPos.x-5 && mouseX < sliders[i].boxPos.x+5 && mouseY > sliders[i].boxPos.y-10 && mouseY < sliders[i].boxPos.y+10) {
      sliders[i].active = true;
    }
  }
  
}

void mouseReleased() {
  for (int i=0; i<sliders.length; i++) {
    sliders[i].active = false;
  }
}

int conSli(float x) {
  int value = int(map(x-860.0, 0, 300, 0, 999));
  return value;
}

void keyPressed() {
  
  for (int i=inputFields.length-1; i>=0; i--) {
    if (inputFields[i].active) {
      if (key == 8 && !inputFields[i].userText.equals("")) {
        inputFields[i].userText = inputFields[i].userText.substring(0, inputFields[i].userText.length()-1);
      } else if (key == '\n' || key == '\t') {
        inputFields[i].active = false;
        if (i < inputFields.length-1) {
          inputFields[i+1].active = true;
          inputFields[i+1].filled = true;
        }
        if (inputFields[i].userText.equals("")) {
          inputFields[i].filled = false;
        }
      } else if (key != CODED) {
        inputFields[i].userText = inputFields[i].userText + key;
      }
    }
  }
  
}
