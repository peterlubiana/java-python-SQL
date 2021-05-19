from nltk.probability import ConditionalFreqDist, ConditionalProbDist, MLEProbDist

TRAIN_DATA = "no_bokmaal-ud-train.tt"
DEV_DATA = "no_bokmaal-ud-dev.tt"


def read_dataset(filename):
    """Read dataset from file and return a list of sentences, each
    sentence a list of words, and a list of the corresponding pos
    tags.
    """

    fil = open(filename, "r")

    sentences = []
    labels = []

    newSentence = []
    newLabelSet = []


    for line in fil:
        # '\n' på starten av en linje markerer ny setning.
        if line == '\n' :
            sentences.append(newSentence)
            labels.append(newLabelSet)
            newSentence = [];
            newLabelSet = [];
            continue
        
        # Hvis det ikke er ny setning lagre ordet og label'en og legg disse 2
        # i setningen som bygges opp.
        line = line.split('\t')
        newSentence.append(line[0])
        newLabelSet.append(line[1].replace('\n',''))

    fil.close();

    return sentences, labels

train_sents, train_labels = read_dataset(TRAIN_DATA)
dev_sents, dev_labels = read_dataset(DEV_DATA)

def bigrams(sequence):
    """Return a sequence of bigrams from input sequence."""

    bgs = [ (sequence[i], sequence[i + 1]) for i in range(0, len(sequence)-1)]
    bgs.insert(0,('<s>',sequence[0]))


    return bgs

class SmoothProbDist(MLEProbDist):
    """Probability distribution with simple smoothing."""

    def prob(self, key):
        """Return probability for key. Add smoothing to zero values."""

        value = super().prob(key)
      
        # Add smoothing here
        if value == 0 :
            value = 1e-20;
        return value

class PosTagger(object):
    """Pos tagger."""

    def __init__(self):
        self.transition = None
        self.emission = None

    def fit(self, sentences, labels):
        """Fit pos tagger to training data."""
        self.transition = ConditionalFreqDist();
        self.emission = ConditionalFreqDist();


        # Setter opp transisjons frekvenser ( PoS gitt en PoS)
        for lab in labels:
            bgs = bigrams(lab)
            for b in bgs:
                self.transition[ b[0] ][ b[1] ] += 1


        # Setter opp emisjons frekvenser ( observasjons frekvenser gitt en PoS )
        for i in range( 0 , len(sentences) - 1 ):
            for j in range( 0 , len(sentences[i]) - 1 ):
                self.emission[ labels[i][j] ][ sentences[i][j] ] += 1

        
        self.transition = ConditionalProbDist(self.transition, MLEProbDist)
        self.emission = ConditionalProbDist(self.emission, SmoothProbDist)


        pass

    
    def transform(self, sentences):


        labels = [] # liste over alle prediksjoner for alle setningene.

        # setter opp en liste over alle mulige tilstandener / Hidden Layers [NOUN, ADP , ... ]
        states = [x for x in self.transition]
        states.remove("<s>");

        # Statistikk mens algoritmen kjører.
        print("Total sentences: ", len(sentences))
        counter = 0;
        percentFinished = 0;





        for sentence in sentences :
            
            # Statistikk mens agoritmen kjører.
            counter+=1;
            val = int(counter/len(sentences)*100);
            if val != percentFinished:
                percentFinished = val
                print(percentFinished," % finished  (",counter,"/",len(sentences),")");


            
            T = len(sentence); # Lagrer lengden på observasjonene i denne setnigen.
            
            viterbi = {}  # oppretter opp Viterbi matrisen.

            # Initialiserer Viterbi matrisen
            for s in states :
                viterbi[s]      = [0 for t in range(0, T)]; # initialiserer viterbi matrisen.
                viterbi[s][0] = self.transition['<s>'].prob(s) * self.emission[s].prob(sentence[0]);
            

            # Rekursjons-steget

            bestPath = [] # list over POS-tags som skal returneres.
            for t in range(1,T):
                bestProb = -1;
                bestState = ""
                for s in states :
                    for state in states :

                        # Kalkulér sannsynligheter
                        newProb = viterbi[state][t - 1] * self.transition[state].prob(s) * self.emission[s].prob(sentence[t]);

                        if newProb > bestProb : # Sjekk om den nye sannsynligheten er max / størst!
                            bestProb = newProb
                            viterbi[s][t] = bestProb
                            bestState = state; # Lagrer den størstmest sannsynlige 
                # Legger til den mest sannsynlige tilstanden i lista som skal returneres. 
                bestPath.append(bestState);
                        
                        
            

            # Terminerings steget.
            bestProb = -1;
            bestLastState = ""
            for s in states:
                if viterbi[s][T-1] > bestProb:  # Finner den mest sannsynlige siste POS-taggen.
                    bestProb = viterbi[s][T-1];
                    bestLastState = s
            
            # Legg til den siste staten i POS-prediksjoner for denne setningen.
            bestPath.append(bestLastState);   
            

            # Legg til POS-prediksjonene for denne setningen i den endelige lista.
            labels.append(bestPath)
            
           
        

        return labels # Returnér POS-tag-prediksjonene for alle setningene.


def accuracy(true, pred):
    """Return accuracy score for predictions."""

    if len(true) != len(pred) :
        return -666
    total = 0
    correct = 0

    # Bla igjennom alle tags i alle setningene
    for i in range(0,len(true)):
        for j in range(0,len(true[i])):
            total += 1
            # Sjekk om tag'ene er like.
            if true[i][j] == pred[i][j] :
                correct += 1

    # returner en accuracy 0-100%
    return ( correct / total) * 100



# Opprett PosTagger for trenings-settet
pt = PosTagger()

# Tren PosTaggeren på trenings-settet
pt.fit(train_sents,train_labels)

# Beregn accuracy på trenings-settet
acc_train = accuracy(train_labels, pt.transform(train_sents))




# Opprett PosTagger for dev-settet
pt2 = PosTagger()

# Tren PosTaggeren på dev-settet
pt2.fit(dev_sents,dev_labels)

# Beregn accuracy på dev-settet
acc_dev   = accuracy(dev_labels, pt2.transform(dev_sents))




# Vis accuracy statistikk.
print("Program over: ")
print('accuracy Dev-set', acc_dev , "%")
print('accuracy Train-set', acc_train , "%")

















