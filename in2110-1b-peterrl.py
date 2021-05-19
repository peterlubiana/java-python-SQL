from in2110.oblig1b import visualize_word_vectors
from in2110.corpora import aviskorpus_10_nn
from math import sqrt


def hentAlleStoppOrd () :
	return ['<s>','</s>','"',"'",'?','<','>','{','}','[',']','+','-','(',')','!!','?!','??','!?','`','``',"''",',','.',':',';','&','%','$','@','!','^','#','*','..','...','alle','andre','at','av','bare','bere','begge','ble','blei','bli','blir','blitt','bort','bra','både','båe','da','de','deg','dei','deim','deira','deires','dem','den','denne','der','dere','deres','deira','det','dette','di','din','disse','ditt','du','dykk','dykkar','då','eg','ei','ein','eit','eitt','eller','elles','en','ene','eneste','einaste','enhver','enkver','kvarein','enn','er','et','ett','etter','for','fordi','fra','frå','få','før','først','fyrst','gjorde','gjøre','god','gå','ha','hadde','han','hans','har','hennar','henne','hennes','her','hjå','ho','hoe','honom','hoss','hossen','hun','hva','hvem','hver','hvilke','hvilken','hvis','hvor','hvordan','hvorfor','i','ikke','ikkje','ingen','ingi','inkje','inn','innen','inni','ja','jeg','kan','kom','korleis','korso','kun','kunne','kva','kvar','kvarhelst','kven','kvi','kvifor','lage','lang','lik','like','makt','man','mange','me','med','medan','meg','mellom','men','mens','mer','mest','mi','min','mine','mitt','mot','mye','mykje','må','måte','ned','nei','no','noe','noen','noka','noko','nokon','nokor','nokre','nå','når','og','også','om','opp','oss','over','på','rett','samme','sant','seg','selv','si','sia','sidan','siden','sin','sine','sist','sitt','sjøl','skal','skulle','slik','slutt','so','som','somme','somt','så','sånn','tid','til','tilbake','um','under','upp','ut','uten','var','vart','varte','ved','vere','verte','vi','vil','ville','vite','vore','vors','vort','vår','være','vært','vore','vört','å'];


def preprocess(sentences):

    """Return list of preprocessed tokens."""

   # Jeg Bruker en  liste over 'stoppord' til å sile ut tegn og ord som 
   # ikke bør være med. En god del tegn men også en del såkalte stoppord, som alle ord vil ende opp med å ha et forhold
   # til fordi de er så enormt frekvente. Så de fjernes.

   # Dette var egentlig implementert som at jeg leste en fil som var lett å konfigurere
   # Men siden obligen krever at vi leverer kun 1 python fil. Så må jeg vel gjøre det da.

    stoppOrdListe = {};

    print("Laster inn stoppord.");
    liste = hentAlleStoppOrd();
    for stoppOrd in liste :
        stoppOrdListe[stoppOrd] = 1;

    # Oppretter en liste for de ferdig pre-prosesserte setningene.
    preprocessedList = [];

    #Printes alle stopp ord / tegn.
    print(stoppOrdListe);

    print("Preprosesserer alle setninger i korpuset:");
    #Bla igjennom alle setninger.
    for sentence in sentences:
        # Gjør setningene til små bokstaver og split setningen opp i tokens. Den semantiske verdien til Mann og mann er jo identisk.
        resultingSentence = sentence.lower().split();
        

        # Fjern stoppord og numeriske ord ( ord som KUN inneholder tall )
        wordsToRemoveFromSentence = [];
        for word in resultingSentence :

            # Fjern ord som kun er nummere.
            if word.isnumeric():
                wordsToRemoveFromSentence.append(word);
                continue;
            
            # Fjern ord/tegn som er i stoppOrdLista.
            try :
                stoppOrdListe[word];
                wordsToRemoveFromSentence.append(word);
            except :
                continue;
                
        #Faktisk fjern de ordene fra hovedsettet.
        for word in wordsToRemoveFromSentence :
            resultingSentence.remove(word);

        #Til slutt legg setningen til blant alle de ferdig pre-prosesserte setningene.
        preprocessedList.append(resultingSentence);

        
    


    return preprocessedList;

def context_window(sent, pos, size):
    """Return context window for word at pos of given size."""

    # Lag en ny liste over ord i konteksten som skal returneres.
    contextList = [];

    # lag en index variabel som sier hvor i setningen vi skal begynne å telle.
    index = pos-size;

    # Hvis indexen endte opp med å bli mindre enn null, må vi starte på null.
    if index < 0 :
        index = 0;

    endIndex = len(sent) - 1;

    # Tell igjennom listen frem til vi er kommet til pos+size som er ordet vi skal finne kontekst for pluss size-antall ord.
    while index <= pos+size and index <= endIndex :
        # skip tokenen / ordet hvis det er det som vinduet gjelder for.
        if index == pos :
            index += 1;
            continue;

        contextList.append(sent[index]);
        index += 1;

    # Returner listen.
    return contextList;





class WordVectorizer(object):
    """Word vectorizer with sklearn-compatible interface."""

    def __init__(self, max_features, window_size, normalize=False):
        self.max_features = max_features
        self.window_size = window_size
        self.normalize = normalize
        self.matrix = None
        self.is_normalized = False

    def fit(self, sentences):
        """Fit vectorizer to sentences."""

        print("Finner mest frekvente ord.");
        frequencyList = {};
        # Hva er de mest frekvente ordene?
        for sentence in sentences :
            for word in sentence :
                if word in frequencyList :
                    frequencyList[word] += 1;
                else :
                    frequencyList[word] = 1;

        self.matrix = {};
        # Sorter frekvenslisten og legg til de mest frekvente ordene i en egen liste.
        print("Sortérer mest frekvente ord.");
        print("Skal lagre ", self.max_features, " ord!" );
        for key, value in sorted(frequencyList.items(), reverse=True, key=lambda list_val: list_val[1]):
            if len(self.matrix) < self.max_features: 
                print("key:" + key + " value :" + str(value) );
                self.matrix[key] = {};
            else : 
                break;


        print("self.matrix er nå en dict over de " + str(len(self.matrix)) +" mest frekvente ordene.");

        print("Setter opp co-occurence matrix'en / ordvektorene.");

        # Loop igjennom alle setningene.
        for sentence in sentences:
            
            # Loop igjennom alle tokenene i hver setning.
            for i in range(0, len(sentence) ):

                # Skip context vindu for ord som ikke er i self.matrix ( som nå inneholder dicts for de mest frekvente ordene ).
                try :
                    self.matrix[sentence[i]];
                except KeyError:
                    continue;


                ## Finn kontekst_vinduet for tokenen / ordet på index i.
                c_window = context_window(sentence,i,self.window_size);
                
                # Loop igjennom hvert ord i hvert context vindu. 
                for word in c_window :
                
                    # Vi vil bare lagre frekvensen av de ordene som er mest brukt.
                    try :
                        self.matrix[word];
                    except KeyError:
                        continue;

                    # Sjekk om en dict-verdi finnes for ordet og inkrementer den.
                    try :
                        self.matrix[sentence[i]][word] += 1;
                    except KeyError:
                    	# Hvis ordet som forekommer i context_window ikke har en egen dict, lag en og sett frekvens til 1.
                        self.matrix[sentence[i]][word] = 1;
                        continue;


                        
        # Normaliserer hvis 'normalize' flagget på WordVectorizer ble initialisert med True.
        if self.normalize :
            self.normalize_vectors();
            print("Vectors were normalized!");   

        pass


    def transform(self, words):
        """Return vectors for each word in words."""

        return [self.matrix[w] for w in words]

    def vector_norm(self, word):
        """Compute vector norm for word."""

        sumVerdier = 0;
        for occuring_word in self.matrix[word] :
            sumVerdier += self.matrix[word][occuring_word] * self.matrix[word][occuring_word];

        return sqrt(sumVerdier);

    def normalize_vectors(self):
        """Normalize vectors."""
        for key in self.matrix :
            vectorLen = self.vector_norm(key);
            for keyInner in self.matrix[key] :
                self.matrix[key][keyInner] = self.matrix[key][keyInner] / vectorLen;


        pass

    def euclidean_distance(self, w1, w2):
        """Compute euclidean distance between w1 and w2."""
        sumVerdier = 0;

        freqWord1 = -1;
        freqWord2 = -1;
        for word in self.matrix:

            # Prøv å aksessere frekvensen til 'word' in ord-vektoren for w1
            try:
                freqWord1 = self.matrix[w1][word];
            except : 
                freqWord1 = 0;
            
            # Prøv å aksessere frekvensen til 'word' in ord-vektoren for w2
            try : 
                freqWord2 = self.matrix[w2][word];
            except :
                freqWord2 = 0;
            
            sumVerdier += pow(freqWord1 - freqWord2,2);

        return sqrt(sumVerdier);

    def cosine_similarity(self, w1, w2):
        """Compute cosine similarity between w1 and w2."""


        # Kun returner dot-product mellom de 2 ordvektorene hvis alle vektorene er normalisert allerede.
        if self.normalize == True :
            return self.vector_norm(w1) * self.vector_norm(w2);

        freqWord1 = -1;
        freqWord2 = -1;
        produktSum = 0;
        for word in self.matrix:
            # Prøv å aksessere frekvensen til 'word' in ord-vektoren for w1
            try:
                freqWord1 = self.matrix[w1][word];
            except : 
                freqWord1 = 0;
            
            # Prøv å aksessere frekvensen til 'word' in ord-vektoren for w2
            try : 
                freqWord2 = self.matrix[w2][word];
            except :
                freqWord2 = 0;

            produktSum += freqWord1 * freqWord2;
        
        return produktSum / (self.vector_norm(w1) * self.vector_norm(w2));

        

    def nearest_neighbors(self, w, k=5):
        """Return list of the k nearest neighbors to w."""
        if not self.isInList(w) :
            return False;

        cos_sim_verdi = 0;
        nearest_neighbors = [];
        for word in self.matrix :

        	# Hvis listen over nærmeste naboer er for liten
        	# legger vi til uansett.
            if len(nearest_neighbors) < k:
                cos_sim_verdi = self.cosine_similarity(w,word);
                nearest_neighbors.append((word , cos_sim_verdi));
                continue;

            # Hvis ordet vi leter etter naboer til er det samme
            # som det vi blar igjennom nå hopp over.
            # Såklart er et ord likest seg selv.
            if word == w:
                continue;

            # Hvis vi er her betyr det at listen inneholder minst k elementer.

            # Først må vi beregne cos_similarityen mellom de 2 ordene.
            cos_sim_verdi = self.cosine_similarity(w,word);

            # Så må sjekke om ulikheten i dette ordet er større enn den minste i lista.
            smallestValInList = 123128989;
            for nn in nearest_neighbors :
                if nn[1] < smallestValInList :
                    smallestValInList = nn[1];
            

            # Hvis denne nye cos_similarity-verdien er større enn den minste verdien
            # Så bytt de ut med hverandre.
            if cos_sim_verdi > smallestValInList : 
                for nn in nearest_neighbors :
                    if smallestValInList == nn[1]:
                        nearest_neighbors.remove(nn);
                        nearest_neighbors.append((word,cos_sim_verdi));
                        break;
                
        

        return nearest_neighbors;

    def isInList(self, word):
        """ Checks wether or not a word is in the list"""
        try :
            self.matrix[word];
        except : 
            return False;
        return True;






## Utfører preprosessering

print("Preprosseserer dataen.");
preProcessedList = preprocess(aviskorpus_10_nn.sentences());


## Lager vectorizeren med et vokabular på 5000 og context-vinduer på 6 ( dvs 3 ord til høyre og venstre for ordet vi søker konteksten for.) .
vec = WordVectorizer(5000,3);


## Kaller fit.
print("Kaller fit på WordVectorizeren.");
vec.fit(preProcessedList);





# Etter at WordVectorizeren har blitt satt opp har jeg laget et slags kommando program.
# Som man kan bruke for å teste WordVectorizeren og funksjonene.


cmd = 0;
while(cmd != "exit") :

    menuString = """ 
\n\nWhat do you wanna do?\n
1 = Search for a word.
2 = Check Co-occurence between two words.
3 = Check Euclidean distance between two words.
4 = Check Cosine_similarity between two words.
5 = Normalize all Vectors. 
6 = Return vector length of a word. 
7 = Print all co-occurences for a word. 
8 = Print the nearest neighbors of a word.
9 = Visualize a set of vectors.
exit = Exit program. \n
 =>  """
    cmd = input(menuString);

    if cmd == "1":
        cmd = input("Search for words matching : ");
        somethingFound = 0;
        for key in vec.matrix:
            if key.find(cmd) != -1:
                print(key);

                if somethingFound == 0 :
                    somethingFound = 1;
        if somethingFound == 0 :
            print("no matches for ", cmd);

        continue;

    if cmd == "2":
        word1 = input("Write a word to check in for occurences. ");
        word2 = input("Write a word for co-occurences with "+word1+"   ");
        if vec.isInList(word1) and vec.isInList(word2) :
            print("vw.matrix[",word1,"][",word2,"] ", str(vec.matrix[word1][word2]));
        else :
            print("Either "+word1, " or ", word2 , " are not in the co-occurencematrix");

        continue;

    if cmd == "3":
        word1 = input("Write a word to check euclidean distance. ");
        word2 = input("Write a word to measure euclidean distance with "+word1+"   ");
        if vec.isInList(word1) and vec.isInList(word2) :
            print("vec.euclidean_distance( ",word1," , ",word2," ) = " , vec.euclidean_distance( word1,word2) );
        else :
            print("Either "+word1, " or ", word2 , " are not in the co-occurencematrix");

        continue;

    if cmd == "4":
        word1 = input("Write a word to check cosine similarity. ");
        word2 = input("Write a word to measure cosine similarity with "+word1+"   ");
        if vec.isInList(word1) and vec.isInList(word2) :
            print("vec.cosine_similarity( ",word1," , ",word2," ) = " , vec.cosine_similarity( word1,word2) );
        else :
            print("Either "+word1, " or ", word2 , " are not in the co-occurencematrix");

        continue;

    if cmd == "5":
        vec.normalize = True;
        vec.normalize_vectors();
        print("\nAll vectors were normalized");       
        continue;

    if cmd == "6":
        word = input("Write the word you want to see the vector-length of => ");
        if vec.isInList(word) :
            print("\nVector length : ", vec.vector_norm(word));
        else:
            print(word, " is not in the list! So you can't see its length. ");
        continue;

    if cmd == "7":
        word = input("Write the word you want to see all co-occurences for => ");
        if vec.isInList(word) :
            wordVector = vec.transform([word]);
            for w in wordVector[0]:
                print("[",word,"][",w,"] = ", wordVector[0][w]);

            print("Antallet co-occurences for dette ordet: ", len(wordVector[0]) );
        else:
            print(word, " is not in the list! So you can't see co-occurence matrix. ");
        continue;

    if cmd == "8":
        word = input("Write the word you want to see see nearest neighbors for => ");
        amount_of_neighbors = input("How many neighbors do you want to see? => ");
        while not amount_of_neighbors.isnumeric() :
            amount_of_neighbors = input("Enter a valid integer please: => ");

        if vec.isInList(word) :
            neighList = vec.nearest_neighbors(word,int(amount_of_neighbors));
            print("Nearest Neighboors of ", word, " : ");
            print(neighList);
        else:
            print(word, " is not in the list! So you can't see its neighbors. ");
        continue;
    if cmd == "9":
        wordList = input("Write a list of words like this word1 word2 word3 word4 => ");
        
        wordList = wordList.split();
        listIsValid = 1;
        for word in wordList :
            if not vec.isInList(word) : 
                listIsValid = 0;
                print("The word ",  word ," is not in the list!");
                break;

        if listIsValid == 0 :
            continue;

        print("Visualizing word vectors .. : ");
        visualize_word_vectors(vec, wordList);





