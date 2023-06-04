using CP;

int pointAmount = 24;

int dostepneRuchy[0..pointAmount][0..pointAmount];

execute {

  var f = new IloOplInputFile("adjacency_matrix.csv");

  var iterator = 0;

  while (!f.eof) {

   var data = f.readline().split(",");

   if (data.length == pointAmount+1 ){

        for(var i=0;i<=pointAmount;i++)

            {

                dostepneRuchy[iterator][i] = data[i]

            }

     iterator = iterator+1;

   }     

  }

  writeln(dostepneRuchy);  

}

int iloscTur = 18;
int dlugoscTrasy = 6;

int indeksGlowicy = 12;
int indeksBramki = 2;
int indeksBramkiPrzeciwnika = 22;

float wspolczynnik = 0.1;

dvar int calaTrasaWMacierzy[0..24][0..24];
dvar int calaTrasaWMacierzyBramkaZero[0..iloscTur][0..24][0..24];
dvar int calaTrasaWMacierzyBramkaJeden[0..iloscTur][0..24][0..24];


dvar int zeroTrasaOdBramkiDoPunktu[0..iloscTur][0..dlugoscTrasy];
dvar int zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[0..iloscTur][0..dlugoscTrasy];
dvar int zeroOstatniIndeksTrasyOdBramki[0..iloscTur];
dvar int zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur[0..iloscTur];
dvar boolean zeroIsZeroBramka[0..iloscTur][0..dlugoscTrasy];


dvar int jedenTrasaOdBramkiDoPunktu[0..iloscTur][0..dlugoscTrasy];
dvar int jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[0..iloscTur][0..dlugoscTrasy];
dvar int jedenOstatniIndeksTrasyOdBramki[0..iloscTur];
dvar int jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur[0..iloscTur];
dvar boolean jedenIsZeroBramkaPrzeciwnik[0..iloscTur][0..dlugoscTrasy];


dvar int trasaWTurzePoWyzerowaniu[0..iloscTur][0..dlugoscTrasy];
dvar int trasaWTurze[0..iloscTur][0..dlugoscTrasy];
dvar int ostatniIndeksTrasyWTurze[0..iloscTur];
dvar int ostatniaTura;
dvar boolean isZero[0..iloscTur][0..dlugoscTrasy];


dvar boolean odwiedzoneWierzcholkiNaPrzestrzeniTur[0..iloscTur][0..34];
dvar int iloscOdwiedzinDanegoWierzcholkaWDanejTurze[0..iloscTur][0..34];
dvar int temp[0..iloscTur][0..dlugoscTrasy];

dvar boolean czyjaTura[0..iloscTur];

dexpr int calaTrasaDlugosc = sum(k in 0..iloscTur) sum(i in 0..dlugoscTrasy-1) dostepneRuchy[trasaWTurze[k][i]][trasaWTurze[k][i+1]];

dexpr int calaTrasaDlugosc2 = sum(i in 0..iloscTur) ostatniIndeksTrasyWTurze[i]; 


dexpr int zeroOdlegloscDoBramki = sum(i in 0..iloscTur) (zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur[i]);

dexpr int jedenOdlegloscDoBramki = sum(i in 0..iloscTur) (jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur[i]);




minimize 99999999999-calaTrasaDlugosc2+ 10 * zeroOdlegloscDoBramki +10* jedenOdlegloscDoBramki + 99-ostatniaTura ;
;

subject to {
	forall(k in 0..iloscTur) forall(g in 0..dlugoscTrasy) odwiedzoneWierzcholkiNaPrzestrzeniTur[k][trasaWTurzePoWyzerowaniu[k][g]] == (k<=ostatniaTura && g<=ostatniIndeksTrasyWTurze[k]);
	forall(k in 0..iloscTur) forall(i in 0..34) (iloscOdwiedzinDanegoWierzcholkaWDanejTurze[k][i] == (sum (g in 0..iloscTur) (g<k && (odwiedzoneWierzcholkiNaPrzestrzeniTur[g][i] >= 1)))); 
    forall(k in 0..iloscTur) forall(i in 0..dlugoscTrasy) temp[k][i] == (isZero[k][i]* (iloscOdwiedzinDanegoWierzcholkaWDanejTurze[k][trasaWTurzePoWyzerowaniu[k][i]])>=1);
    forall(k in 1..iloscTur) forall(i in 0..dlugoscTrasy) temp[k][i] == (i < ostatniIndeksTrasyWTurze[k]);
    czyjaTura[0] == 1;
    ostatniIndeksTrasyWTurze[0] == 1;
    ostatniIndeksTrasyWTurze[1] == 1;
    trasaWTurze[0][0] == indeksGlowicy;
    forall(i in 0..iloscTur) forall(j in 0..dlugoscTrasy) (1-czyjaTura[i] * trasaWTurzePoWyzerowaniu[i][j] != indeksBramkiPrzeciwnika);
    forall(i in 0..iloscTur) forall(j in 0..dlugoscTrasy) (czyjaTura[i] * trasaWTurzePoWyzerowaniu[i][j] != indeksBramki);
    forall(i in 0..iloscTur) zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur[i] == ((1-czyjaTura[i]) * zeroOstatniIndeksTrasyOdBramki[i]) * (ostatniaTura > i);
    forall(i in 0..iloscTur) jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur[i] == (czyjaTura[i] * jedenOstatniIndeksTrasyOdBramki[i]) *(ostatniaTura> i);
    forall(i in 0..iloscTur) forall(j in 0..dlugoscTrasy) trasaWTurzePoWyzerowaniu[i][j] == isZero[i][j] * trasaWTurze[i][j]; 
    forall(i in 0..iloscTur)forall(j in 0..dlugoscTrasy-1)(calaTrasaWMacierzy[trasaWTurzePoWyzerowaniu[i][j]][trasaWTurzePoWyzerowaniu[i][j+1]] ==(sum(k in 0..iloscTur) sum(g in 0..dlugoscTrasy-1) (trasaWTurzePoWyzerowaniu[i][j] == trasaWTurzePoWyzerowaniu[k][g] && trasaWTurzePoWyzerowaniu[i][j+1] ==trasaWTurzePoWyzerowaniu[k][g+1])));
    forall(i in 0..iloscTur)forall(j in 1..dlugoscTrasy)(calaTrasaWMacierzy[trasaWTurzePoWyzerowaniu[i][j-1]][trasaWTurzePoWyzerowaniu[i][j]] ==(sum(k in 0..iloscTur) sum(g in 1..dlugoscTrasy) (trasaWTurzePoWyzerowaniu[i][j] == trasaWTurzePoWyzerowaniu[k][g] && trasaWTurzePoWyzerowaniu[i][j-1] ==trasaWTurzePoWyzerowaniu[k][g-1])));
    forall(i in 0..iloscTur)forall(j in 0..dlugoscTrasy-1)(calaTrasaWMacierzyBramkaZero[i][zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j]][zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j+1]] ==(sum(g in 0..dlugoscTrasy-1) (zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j] == zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g] && zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j+1] ==zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g+1])));
    forall(i in 0..iloscTur) forall(j in 1..dlugoscTrasy)(calaTrasaWMacierzyBramkaZero[i][zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j-1]][zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j]] ==(sum(g in 1..dlugoscTrasy) (zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j] == zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g] && zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j-1] ==zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g-1])));
    forall(i in 0..iloscTur)forall(j in 0..dlugoscTrasy-1)(calaTrasaWMacierzyBramkaJeden[i][jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j]][jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j+1]] ==(sum(g in 0..dlugoscTrasy-1) (jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j] == jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g] && jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j+1] ==jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g+1])));
    forall(i in 0..iloscTur)forall(j in 1..dlugoscTrasy)(calaTrasaWMacierzyBramkaJeden[i][jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j-1]][jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j]] ==(sum(g in 1..dlugoscTrasy) (jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j] == jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g] && jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j-1] ==jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][g-1])));
    ostatniaTura >= 1;
    forall(i in 1..24) forall(j in 1..24) calaTrasaWMacierzy[i][j] <= 1;
    forall(i in 1..24) calaTrasaWMacierzy[i][0] <= 1;
    forall(i in 1..24) calaTrasaWMacierzy[0][i] <= 1;
    forall(i in 1..24) forall(j in 1..24) (calaTrasaWMacierzy[i][j] + calaTrasaWMacierzy[j][i]) <=1;
    forall(i in 1..24) (calaTrasaWMacierzy[i][0] + calaTrasaWMacierzy[0][i]) <=1;
    forall(k in 0..iloscTur)forall(i in 1..24) forall(j in 1..24) calaTrasaWMacierzyBramkaZero[k][i][j] <= 1;
    forall(k in 0..iloscTur)forall(i in 1..24) calaTrasaWMacierzyBramkaZero[k][i][0] <= 1;
    forall(k in 0..iloscTur)forall(i in 1..24) forall(j in 1..24) (calaTrasaWMacierzyBramkaZero[k][i][j] + calaTrasaWMacierzyBramkaZero[k][j][i]) <=1;
    forall(k in 0..iloscTur)forall(i in 1..24) (calaTrasaWMacierzyBramkaZero[k][i][0] + calaTrasaWMacierzyBramkaZero[k][0][i]) <=1;
    forall(k in 0..iloscTur)forall(i in 1..24) forall(j in 1..24) calaTrasaWMacierzyBramkaJeden[k][i][j] <= 1;
    forall(k in 0..iloscTur)forall(i in 1..24) calaTrasaWMacierzyBramkaJeden[k][i][0] <= 1;
    forall(k in 0..iloscTur)forall(i in 1..24) forall(j in 1..24) (calaTrasaWMacierzyBramkaJeden[k][i][j] + calaTrasaWMacierzyBramkaJeden[k][j][i]) <=1;
    forall(k in 0..iloscTur)forall(i in 1..24) (calaTrasaWMacierzyBramkaJeden[k][i][0] + calaTrasaWMacierzyBramkaJeden[k][0][i]) <=1;
    forall(i in 0..iloscTur-1)(trasaWTurze[i+1][0] == trasaWTurze[i][ostatniIndeksTrasyWTurze[i]]);
    forall(i in 0..iloscTur-1) czyjaTura[i+1] == 1-czyjaTura[i];
    forall(k in 0..iloscTur) forall(i in 0..dlugoscTrasy-1) (dostepneRuchy[trasaWTurze[k][i]][trasaWTurze[k][i+1]] != 0);
    forall(i in 0..iloscTur) zeroTrasaOdBramkiDoPunktu[i][0] == trasaWTurze[i][ostatniIndeksTrasyWTurze[i]];
    forall(k in 0..iloscTur) forall(i in 0..dlugoscTrasy-1) (dostepneRuchy[zeroTrasaOdBramkiDoPunktu[k][i]][zeroTrasaOdBramkiDoPunktu[k][i+1]] != 0);
    forall(i in 0..iloscTur) zeroTrasaOdBramkiDoPunktu[i][zeroOstatniIndeksTrasyOdBramki[i]] == indeksBramki;
    forall(i in 0..iloscTur) forall(j in 0..dlugoscTrasy) zeroTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j] == zeroIsZeroBramka[i][j] * zeroTrasaOdBramkiDoPunktu[i][j]; 
    forall(i in 0..iloscTur) jedenTrasaOdBramkiDoPunktu[i][0] == trasaWTurze[i][ostatniIndeksTrasyWTurze[i]];
    forall(k in 0..iloscTur) forall(i in 0..dlugoscTrasy-1) (dostepneRuchy[jedenTrasaOdBramkiDoPunktu[k][i]][jedenTrasaOdBramkiDoPunktu[k][i+1]] != 0);
    forall(i in 0..iloscTur) jedenTrasaOdBramkiDoPunktu[i][jedenOstatniIndeksTrasyOdBramki[i]] == indeksBramkiPrzeciwnika;
    forall(i in 0..iloscTur) forall(j in 0..dlugoscTrasy) jedenTrasaOdBramkiDoPunktuPoWyzerowaniu[i][j] == jedenIsZeroBramkaPrzeciwnik[i][j] * jedenTrasaOdBramkiDoPunktu[i][j]; 
//  jezeli chcemy wymusic koniec w jednej z dwoch bramek
//  trasaWTurze[ostatniaTura][ostatniIndeksTrasyWTurze[ostatniaTura]] == czyjaTura[ostatniaTura] * indeksBramkiPrzeciwnika + (1-czyjaTura[ostatniaTura]) * indeksBramki;
    ostatniaTura <= iloscTur;
    forall(i in 0..iloscTur) ostatniIndeksTrasyWTurze[i] > 0;
    forall(i in 0..iloscTur) ostatniIndeksTrasyWTurze[i] <= dlugoscTrasy;
    forall(i in 0..iloscTur) zeroOstatniIndeksTrasyOdBramki[i] <= dlugoscTrasy;
    forall(i in 0..iloscTur) jedenOstatniIndeksTrasyOdBramki[i] <= dlugoscTrasy;
    forall(i in 0..iloscTur) {
        forall(j in 0..dlugoscTrasy) {
            isZero[i][j] == ((i <= ostatniaTura) && (j <= ostatniIndeksTrasyWTurze[i]));
            zeroIsZeroBramka[i][j] == (czyjaTura[i] == 0 && (j <= zeroOstatniIndeksTrasyOdBramki[i]));
            jedenIsZeroBramkaPrzeciwnik[i][j] == (czyjaTura[i] == 1 && (j <= jedenOstatniIndeksTrasyOdBramki[i]));
          }    
    }  

}