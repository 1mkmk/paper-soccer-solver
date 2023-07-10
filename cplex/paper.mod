using CP;

int pointAmount = 24;

int availableMoves[0..pointAmount][0..pointAmount];

execute {
  var f = new IloOplInputFile("adjacency_matrix.csv");

  var iterator = 0;

  while (!f.eof) {
    var data = f.readline().split(",");

    if (data.length == pointAmount + 1) {
      for (var i = 0; i <= pointAmount; i++) {
        availableMoves[iterator][i] = data[i];
      }
      iterator = iterator + 1;
    }
  }

  writeln(availableMoves);
}

int numberOfTurns = 18;
int routeLength = 6;

int headIndex = 12;
int gateIndex = 2;
int opponentGateIndex = 22;

float coefficient = 0.1;

dvar int wholeRouteInMatrix[0..24][0..24];
dvar int wholeRouteInMatrixGateZero[0..numberOfTurns][0..24][0..24];
dvar int wholeRouteInMatrixGateOne[0..numberOfTurns][0..24][0..24];

dvar int zeroRouteFromGateToPoint[0..numberOfTurns][0..routeLength];
dvar int zeroRouteFromGateToPointAfterZeroing[0..numberOfTurns][0..routeLength];
dvar int zeroLastIndexInRouteFromGate[0..numberOfTurns];
dvar int zeroLastIndexInRouteFromGateAfterConsideringTurns[0..numberOfTurns];
dvar boolean zeroIsZeroGate[0..numberOfTurns][0..routeLength];

dvar int oneRouteFromGateToPoint[0..numberOfTurns][0..routeLength];
dvar int oneRouteFromGateToPointAfterZeroing[0..numberOfTurns][0..routeLength];
dvar int oneLastIndexInRouteFromGate[0..numberOfTurns];
dvar int oneLastIndexInRouteFromGateAfterConsideringTurns[0..numberOfTurns];
dvar boolean oneIsZeroOpponentGate[0..numberOfTurns][0..routeLength];

dvar int routeInTurnAfterZeroing[0..numberOfTurns][0..routeLength];
dvar int routeInTurn[0..numberOfTurns][0..routeLength];
dvar int lastIndexOfRouteInTurn[0..numberOfTurns];
dvar int lastTurn;
dvar boolean isZero[0..numberOfTurns][0..routeLength];

dvar boolean visitedVerticesOverTurns[0..numberOfTurns][0..34];
dvar int numberOfVisitsToVertexInTurn[0..numberOfTurns][0..34];
dvar int temp[0..numberOfTurns][0..routeLength];

dvar boolean whoseTurn[0..numberOfTurns];

dexpr int wholeRouteLength = sum(k in 0..numberOfTurns) sum(i in 0..routeLength - 1) availableMoves[routeInTurn[k][i]][routeInTurn[k][i + 1]];

dexpr int wholeRouteLength2 = sum(i in 0..numberOfTurns) lastIndexOfRouteInTurn[i];

dexpr int zeroDistanceToGate = sum(i in 0..numberOfTurns) (zeroLastIndexInRouteFromGateAfterConsideringTurns[i]);

dexpr int oneDistanceToGate = sum(i in 0..numberOfTurns) (oneLastIndexInRouteFromGateAfterConsideringTurns[i]);

minimize 99999999999 - wholeRouteLength2 + 10 * zeroDistanceToGate + 10 * oneDistanceToGate + 99 - lastTurn;
;

subject to {
  forall(k in 0..numberOfTurns) forall(g in 0..routeLength) visitedVerticesOverTurns[k][routeInTurnAfterZeroing[k][g]] == (k <= lastTurn && g <= lastIndexOfRouteInTurn[k]);
  forall(k in 0..numberOfTurns) forall(i in 0..34) (numberOfVisitsToVertexInTurn[k][i] == (sum(g in 0..numberOfTurns) (g < k && (visitedVerticesOverTurns[g][i] >= 1))));
  forall(k in 0..numberOfTurns) forall(i in 0..routeLength) temp[k][i] == (isZero[k][i] * (numberOfVisitsToVertexInTurn[k][routeInTurnAfterZeroing[k][i]]) >= 1);
  forall(k in 1..numberOfTurns) forall(i in 0..routeLength) temp[k][i] == (i < lastIndexOfRouteInTurn[k]);
  whoseTurn[0] == 1;
  lastIndexOfRouteInTurn[0] == 1;
  lastIndexOfRouteInTurn[1] == 1;
  routeInTurn[0][0] == headIndex;
  forall(i in 0..numberOfTurns) forall(j in 0..routeLength) (1 - whoseTurn[i] * routeInTurnAfterZeroing[i][j] != opponentGateIndex);
  forall(i in 0..numberOfTurns) forall(j in 0..routeLength) (whoseTurn[i] * routeInTurnAfterZeroing[i][j] != gateIndex);
  forall(i in 0..numberOfTurns) zeroLastIndexInRouteFromGateAfterConsideringTurns[i] == ((1 - whoseTurn[i]) * zeroLastIndexInRouteFromGate[i]) * (lastTurn > i);
  forall(i in 0..numberOfTurns) oneLastIndexInRouteFromGateAfterConsideringTurns[i] == (whoseTurn[i] * oneLastIndexInRouteFromGate[i]) * (lastTurn > i);
  forall(i in 0..numberOfTurns) forall(j in 0..routeLength) routeInTurnAfterZeroing[i][j] == isZero[i][j] * routeInTurn[i][j];
  forall(i in 0..numberOfTurns) forall(j in 0..routeLength - 1) (wholeRouteInMatrix[routeInTurnAfterZeroing[i][j]][routeInTurnAfterZeroing[i][j + 1]] == (sum(k in 0..numberOfTurns) sum(g in 0..routeLength - 1) (routeInTurnAfterZeroing[i][j] == routeInTurnAfterZeroing[k][g] && routeInTurnAfterZeroing[i][j + 1] == routeInTurnAfterZeroing[k][g + 1])));
  forall(i in 0..numberOfTurns) forall(j in 1..routeLength) (wholeRouteInMatrix[routeInTurnAfterZeroing[i][j - 1]][routeInTurnAfterZeroing[i][j]] == (sum(k in 0..numberOfTurns) sum(g in 1..routeLength) (routeInTurnAfterZeroing[i][j] == routeInTurnAfterZeroing[k][g] && routeInTurnAfterZeroing[i][j - 1] == routeInTurnAfterZeroing[k][g - 1])));
  forall(i in 0..numberOfTurns) forall(j in 0..routeLength - 1) (wholeRouteInMatrixGateZero[i][j] <= 1;
  forall(i in 1..24) forall(j in 1..24) (wholeRouteInMatrix[i][j] + wholeRouteInMatrix[j][i]) <= 1;
  forall(i in 1..24) (wholeRouteInMatrix[i][0] + wholeRouteInMatrix[0][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) wholeRouteInMatrixGateZero[k][i][j] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) wholeRouteInMatrixGateZero[k][i][0] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) (wholeRouteInMatrixGateZero[k][i][j] + wholeRouteInMatrixGateZero[k][j][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) (wholeRouteInMatrixGateZero[k][i][0] + wholeRouteInMatrixGateZero[k][0][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) wholeRouteInMatrixGateOne[k][i][j] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) wholeRouteInMatrixGateOne[k][i][0] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) (wholeRouteInMatrixGateOne[k][i][j] + wholeRouteInMatrixGateOne[k][j][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) (wholeRouteInMatrixGateOne[k][i][0] + wholeRouteInMatrixGateOne[k][0][i]) <= 1;
  forall(i in 0..numberOfTurns - 1) (routeInTurn[i + 1][0] == routeInTurn[i][lastIndexOfRouteInTurn[i]]);
  forall(i in 0..numberOfTurns - 1) whoseTurn[i + 1] == 1 - whoseTurn[i];
  forall(k in 0..numberOfTurns) forall(i in 0..routeLength - 1) (availableMoves[routeInTurn[k][i]][routeInTurn[k][i + 1]] != 0);
  forall(i in 0..numberOfTurns) zeroRouteFromGateToPoint[i][0] == routeInTurn[i][lastIndexOfRouteInTurn[i]];
  forall(k in 0..numberOfTurns) forall(i in 0..routeLength - 1) (availableMoves[zeroRouteFromGateToPoint[k][i]][zeroRouteFromGateToPoint[k][i + 1]] != 0);
  forall(i in 0..numberOfTurns) zeroRouteFromGateToPoint[i][zeroLastIndexInRouteFromGate[i]] == gateIndex;
  forall(i in 0..numberOfTurns) forall(j in 0..routeLength) zeroRouteFromGateToPointAfterZeroing[i][j] == zeroIsZeroGate[i][j] * zeroRouteFromGateToPoint[i][j];
  forall(i in 0..numberOfTurns) oneRouteFromGateToPoint[i][0] == routeInTurn[i][lastIndexOfRouteInTurn[i]];
  forall(k in 0..numberOfTurns) forall(i in 0..routeLength - 1) (availableMoves[oneRouteFromGateToPoint[k][i]][oneRouteFromGateToPoint[k][i + 1]] != 0);
  forall(i in 0..numberOfTurns) oneRouteFromGateToPoint[i][oneLastIndexInRouteFromGate[i]] == opponentGateIndex;
  forall(i in 0..numberOfTurns) forall(j in 0..routeLength) oneRouteFromGateToPointAfterZeroing[i][j] == oneIsZeroOpponentGate[i][j] * oneRouteFromGateToPoint[i][j];
  lastTurn >= 1;
  forall(i in 1..24) forall(j in 1..24) wholeRouteInMatrix[i][j] <= 1;
  forall(i in 1..24) wholeRouteInMatrix[i][0] <= 1;
  forall(i in 1..24) forall(j in 1..24) (wholeRouteInMatrix[i][j] + wholeRouteInMatrix[j][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) wholeRouteInMatrixGateZero[k][i][j] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) wholeRouteInMatrixGateZero[k][i][0] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) (wholeRouteInMatrixGateZero[k][i][j] + wholeRouteInMatrixGateZero[k][j][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) (wholeRouteInMatrixGateZero[k][i][0] + wholeRouteInMatrixGateZero[k][0][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) wholeRouteInMatrixGateOne[k][i][j] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) wholeRouteInMatrixGateOne[k][i][0] <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) forall(j in 1..24) (wholeRouteInMatrixGateOne[k][i][j] + wholeRouteInMatrixGateOne[k][j][i]) <= 1;
  forall(k in 0..numberOfTurns) forall(i in 1..24) (wholeRouteInMatrixGateOne[k][i][0] + wholeRouteInMatrixGateOne[k][0][i]) <= 1;
  forall(i in 0..numberOfTurns) (routeInTurn[i][0] == headIndex);
  forall(i in 0..numberOfTurns) (lastIndexOfRouteInTurn[i] > 0);
  forall(i in 0..numberOfTurns) (lastIndexOfRouteInTurn[i] <= routeLength);
  forall(i in 0..numberOfTurns) (zeroLastIndexInRouteFromGate[i] <= routeLength);
  forall(i in 0..numberOfTurns) (oneLastIndexInRouteFromGate[i] <= routeLength);
  forall(i in 0..numberOfTurns) {
    forall(j in 0..routeLength) {
      isZero[i][j] == ((i <= lastTurn) && (j <=lastIndexOfRouteInTurn[i]);
      zeroIsZeroGate[i][j] <= 1;
      oneIsZeroOpponentGate[i][j] <= 1;
      zeroRouteFromGateToPointAfterZeroing[i][j] <= routeLength;
      oneRouteFromGateToPointAfterZeroing[i][j] <= routeLength;
    }
  }
  forall(i in 0..numberOfTurns) {
    zeroRouteFromGateToPoint[i][0] == routeInTurn[i][lastIndexOfRouteInTurn[i]];
    zeroRouteFromGateToPointAfterZeroing[i][0] == zeroRouteFromGateToPoint[i][0];
    oneRouteFromGateToPoint[i][0] == routeInTurn[i][lastIndexOfRouteInTurn[i]];
    oneRouteFromGateToPointAfterZeroing[i][0] == oneRouteFromGateToPoint[i][0];
  }
  forall(i in 0..numberOfTurns) {
    forall(j in 0..routeLength - 1) {
      zeroRouteFromGateToPoint[i][j + 1] == routeInTurn[i][j];
      zeroRouteFromGateToPointAfterZeroing[i][j + 1] == zeroRouteFromGateToPoint[i][j + 1] * (1 - zeroIsZeroGate[i][j + 1]);
      oneRouteFromGateToPoint[i][j + 1] == routeInTurn[i][j];
      oneRouteFromGateToPointAfterZeroing[i][j + 1] == oneRouteFromGateToPoint[i][j + 1] * (1 - oneIsZeroOpponentGate[i][j + 1]);
    }
  }
  forall(k in 0..numberOfTurns) {
    forall(i in 0..routeLength) {
      zeroRouteFromGateToPointAfterZeroing[k][i] >= 0;
      oneRouteFromGateToPointAfterZeroing[k][i] >= 0;
    }
  }
  forall(k in 0..numberOfTurns) {
    zeroRouteFromGateToPointAfterZeroing[k][zeroLastIndexInRouteFromGateAfterConsideringTurns[k]] == gateIndex;
    oneRouteFromGateToPointAfterZeroing[k][oneLastIndexInRouteFromGateAfterConsideringTurns[k]] == opponentGateIndex;
  }
  lastTurn >= 1;
  forall(i in 1..24) {
    forall(j in 1..24) {
      wholeRouteInMatrix[i][j] <= 1;
      wholeRouteInMatrix[j][i] <= 1;
    }
  }
  forall(i in 1..24) {
    wholeRouteInMatrix[i][0] <= 1;
    wholeRouteInMatrix[0][i] <= 1;
  }
  forall(k in 0..numberOfTurns) {
    forall(i in 1..24) {
      forall(j in 1..24) {
        wholeRouteInMatrixGateZero[k][i][j] <= 1;
        wholeRouteInMatrixGateZero[k][j][i] <= 1;
      }
    }
    forall(i in 1..24) {
      wholeRouteInMatrixGateZero[k][i][0] <= 1;
      wholeRouteInMatrixGateZero[k][0][i] <= 1;
    }
  }
  forall(k in 0..numberOfTurns) {
    forall(i in 1..24) {
      forall(j in 1..24) {
        wholeRouteInMatrixGateOne[k][i][j] <= 1;
        wholeRouteInMatrixGateOne[k][j][i] <= 1;
      }
    }
    forall(i in 1..24) {
      wholeRouteInMatrixGateOne[k][i][0] <= 1;
      wholeRouteInMatrixGateOne[k][0][i] <= 1;
    }
  }
  forall(k in 0..numberOfTurns) {
    forall(i in 0..routeLength - 1) {
      forall(j in 0..routeLength - 1) {
        wholeRouteInMatrixGateZero[k][zeroRouteFromGateToPoint[k][i]][zeroRouteFromGateToPoint[k][i + 1]] >= Zero[k][j];
        wholeRouteInMatrixGateOne[k][oneRouteFromGateToPoint[k][i]][oneRouteFromGateToPoint[k][i + 1]] >= One[k][j];
      }
    }
  }
}