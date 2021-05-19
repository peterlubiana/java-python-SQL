import java.util.Stack;
import java.util.Arrays;
import java.util.HashMap;

class Oblig3{
	

	public static void main(String[] args){


		// Konfigurasjon for testtingen av sorterings algoritmene.

		// Algoritmene som skal kjøres.
		 String[] algorithms = {
		 	 "selectionsort", 
		 	 "insertionsort", 
		 	 "bucketsort", 
		 	"quicksort", 
		 	 "java.util.Arrays.sort" 
		 };

		// Hvordan inputen til sorteringsalgoritmene er sortert når
		// sorteringen starter.
		String[] inputKinds = {
			"random", 
			"ascending", 
			"descending" 
		};

		// Hvilke størrelser på input som skal sorteres.
		int[] inputSizes    = {
			 10,
			 1000, 
			 5000, 
			 10000, 
			 50000, 
			 100000, 
			 500000
		};

		// Faktisk utføring av alle sorteringstestene basert på konfigurasjonen
		// Like over.
		for (String alg : algorithms){
			for(String input : inputKinds){
				for(int elCount : inputSizes){
					testSortByAlgorithmInputKindAndCount(alg,input,elCount,true) ;
				}
			}
		}



	}


	// Starter å ta tiden, kjøretiden kan hentes med getTime()
	public static long t = System.nanoTime();
	public static void restartTimer(){
		t = System.nanoTime(); // nanosek
	}

	// Returnerer tiden siden forrige restartTimer() kall.
	public static double getTime(){
		return (System.nanoTime()-t)/10000000.0;
	}


	/*
		Metode som gjør det mulig å fleksibelt kalle en av flere sorteringsalgoritmer med en angitt input størrelse
		og hvordan input dataen skal være forhåndssortert.
	*/
	public static double testSortByAlgorithmInputKindAndCount(String sortAlgorithm, String inputKind, int elementCount, boolean printExtra){

		// Lag array.
		int[] arr = getIntArray(inputKind ,elementCount);

		// Pretty print ekstra informasjon om sorteringen som er i ferd med å skje.
		if(printExtra){
			System.out.println(sortAlgorithm+" "+inputKind+" order:");
			System.out.println("________________________");
		}
		
		
		// Start timer
		restartTimer();
		arr = Sorter.sort(arr,sortAlgorithm); // utfør angitt sortering.
		double time = getTime(); // les av tiden

		// Print resultater
		if(printExtra) {
			System.out.println( "\nresults: "+ elementCount+ " ints sorted with: "+sortAlgorithm+" ordering: "+inputKind);
			
			// Bare print tiden hvis antallet er 10 eller mindre. 
			// Så det ikke blir så overfylt med tall på skjermen.
			if(elementCount <= 10 ) 
				printArray("",arr);
		}
		

		System.out.println("time spent: " + time);
		System.out.println("\n\n");
		return time;


	}
		

	public static java.util.Random rand = new java.util.Random();
	
	// Random metode returnerer en int mellom 0 og a inkl. 0.
	public static int getRandom(int a){
		return rand.nextInt(a);
	}

	// Random metode returnerer en int mellom a og b.
	public static int getRandom(int a, int b){
		return rand.nextInt((1+b)-a) + a;
	}
	

	// Returnerer et int[], stigende, synkende eller tilfeldig sortert med amountOfElements antall elementer i.
	public static int[] getIntArray(String kind, int amountOfElements){
		int[] arr = new int[amountOfElements];
		Stack<Integer> stack = new Stack<Integer>(); 
		int k = 0;
		while(k < amountOfElements)
			stack.push(new Integer(k++));
		
		


		for(int i = 0; i < amountOfElements; i++){

			if(kind.equals("ascending")) arr[i] = stack.get(i).intValue();

			if(kind.equals("descending")) arr[i] = stack.pop().intValue();

			if(kind.equals("random")){
				
				arr[i] = stack.remove(getRandom(stack.size())).intValue();
			}

		}
		return arr;
	}

	// Printer et int[] array på en lettleselig måte, man kan spesifisere en startmelding som forekommer
	// Like før arrayet printes ut.
	public static void printArray(String startMessage, int[] arr){
		System.out.println(startMessage);
		System.out.print("Array> ");
		for(int i = 0 ; i < arr.length ; i++){
			System.out.print(arr[i]);
			if(i != arr.length-1){
				System.out.print(", ");
			}
		}
		System.out.println();
		System.out.println();
	}

	// Printer et int[] array på en lettleselig måte, man kan spesifisere en startmelding som forekommer
	// Like før arrayet printes ut, ogs en tilsvarende sluttmelding.
	public static void printArray(String startMessage, int[] arr, String endMessage){
		printArray(startMessage,arr);
		System.out.println(endMessage);
	}


}





/*
*  Klasse som inneholder alle sorteringsalgoritmene i Oblig 3 og nyttemetoder for sortering.
*/
class Sorter{
	
	// Generell sorteringsmetode som gjør det lettere å kalle en spesifisert sorteringsmetode.
	public static int[] sort(int[] arr, String method){
		
			if(method.equals("quicksort")) return quickSort(arr);
			if(method.equals("selectionsort")) return selectionSort(arr);
			if(method.equals("bucketsort")) return bucketSort(arr);
			if(method.equals("insertionsort")) return insertionSort(arr);
			if(method.equals("java.util.Arrays.sort")) java.util.Arrays.sort(arr);
			return arr;
		
	}

	// Hjelpemetode for quickSort som hjelper oss med å holde metode kallet generisk når man bruker
	// Sorter.sort(int[] arr,"quickSort").
	public static int[] quickSort(int[] arr){
		
		if(arr.length == 0 || arr.length == 1 || arr == null)
		return arr;
		
		// Finn min og max verdien i quickSort og kall correctInPlaceQuickSort med de verdiene
		int min = arr[0];
		int max = arr[0];
		for(int i : arr){
			if(i < min) min = i;
			if(i > max ) max = i;
		}

		// Faktisk kall på den reelle Quick-sort sorteringen.
		return correctInPlaceQuickSort(arr, min, max);
	}


	/*
		Algorithm correctInPlaceQuickSort(S, a, b):
		Input: An array, S, of distinct elements; integers a and b 
		Output: The subarray S[a .. b] arranged in nondecreasing order
		
		while a < b do
			l ← inPlacePartition(S, a, b)   // from Algorithm 8.9 
			if l − a < b − l then 			//firstsubarrayissmaller
				CorrectInPlaceQuickSort(S, a, l − 1)
				a ← l + 1 
			else
				CorrectInPlaceQuickSort(S, l + 1, b)
			 	b ← l − 1
	*/


	// 'tail'- Rekursiv quicksort som ikke står i fare for å konsumere 
	// for mye av stack-minnet. Følger oppskriften like over som var i boka.
	public static int[] correctInPlaceQuickSort(int [] arr, int a, int b){
		

		int l;
	 	while ( a < b){
	 		l = inPlacePartition(arr, a, b);
	 		if(l - a < b - l ){
	 			correctInPlaceQuickSort(arr, a, l - 1 );
	 			a = l + 1;
	 		}else{
	 			correctInPlaceQuickSort(arr, l + 1, b);
	 			b = l - 1;
	 		}
	 		//Oblig3.printArray("iteration: ",arr);
	 	}


		return arr;
	}




	/*Algorithm inPlacePartition(S, a, b):
		Input: An array, S, of distinct elements; integers a and b such that a ≤ b 
		Output: Aninteger,l,suchthatthesubarrayS[a..b]ispartitionedintoS[a..l−
		1] and S[l..b] so that every element in S[a..l − 1] is less than each element in S[l..b]


		Let r be a random integer in the range [a, b] 
		Swap S[r] and S[b]
		p ← S[b]				// the pivot
		l ← a 					// l will scan rightward
		r ← b − 1				// r will scan leftward

		while l ≤ r do {// find an element larger than the pivot
		
		
		
			while l ≤ r and S[l] ≤ p do 
				l ← l + 1

			while r ≥ l and S[r] ≥ p do	// find an element smaller than the pivot
				r←r−1
			if l < r then
				Swap S[l] and S[r]
		}
		
		Swap S[l] and S[b] // put the pivot into its final place 

		return l
	*/

	// Hjelpemetode for quicksort som løser en subdel av sorteringsproblemet til
	// correctInPlaceQuickSort ved bruk av pivot / oppdeling på et tilfeldig generert heltall.
	// Følger oppskriften hentet fra boka, som er i kommentar like over
	public static int inPlacePartition(int[] arr, int a, int b){


		int r = Oblig3.getRandom(a,b); //Genererer tilfeldig pivot punkt heltall mellom a og b.

		int temp = arr[b];  
		arr[b] = arr[r];
		arr[r] = temp;

		int p = arr[b];
		int l = a;
		r = b - 1;

		

		while(l <= r){

			while(l <= r && arr[l] <= p){
				l = l + 1;
			}

			while(r >= l && arr[r] >= p){
				r = r - 1;
			}
			if(l < r){
				temp = arr[l];
				arr[l] = arr[r];
				arr[r] = temp;
			}

		}

		temp = arr[l];
		arr[l] = arr[b];
		arr[b] = temp;
		



		return l;
	}






	/*
			Algorithm InsertionSort(A):
			Input: An array, A, of n comparable elements, indexed from 1 to n 

			Output: An ordering of A so that its elements are in nondecreasing order.


			for i ← 2 to n do 
				x ← A[i]
				
				// Put x in the right place in A[1..i], moving larger elements up as needed. 

				j←i

				while j > 1 and x < A[j − 1] do
				
					A[j] ← A[j − 1] // move A[j − 1] up one cell
				
					j←j−1 

				A[j] ← x

			return A
		*/
			
	
	// Insertion-sort implementert etter lærebokas oppskrift i kommentaren over.
	public static int[] insertionSort(int [] arr){
		
			int x, j;
			for(int i = 0 ; i < arr.length ; i++){
				x = arr[i];
				j = i;

				while(j > 0 && x < arr[j-1]){
					arr[j] = arr[j-1];
					j = j - 1;
				}

				arr[j] = x;
				//Oblig3.printArray("iteration:", arr);
			}


		return arr;
	}
	




	/*

		Algorithm bucketSort(S):
		Input: Sequence S of items with integer keys in the range [0, N − 1] 

		Output: Sequence S sorted in nondecreasing order of the keys
		

		let B be an array of N lists, each of which is initially empty 

		for each item x in S do
			let k be the key of x
			remove x from S and insert it at the end of bucket (list) B[k] 

		for i ← 0 to N − 1 do
			for each item x in list B[i] do
				remove x from B[i] and insert it at the end of S

		*/

	// Raskere Bucket-sort tilpasset int[]. Er implementert inspirert av 
	// oppskriften over, men gjort uten å lage egene lister som lagrer hver faktiske int verdi.
	// Snarere bare antall forekomster.
	public static int[] bucketSort(int [] arr){
		

		
		int[] B = new int[arr.length]; // Med heltall NØKLER i rekkevidden [ 0, N - 1];


		int i = 0;
		for(int key = 0 ; key < arr.length ; key++){
			B[arr[key]] += 1; // Hvis verdien til arr[key] var f.eks 10 og input arrayet faktisk inneholder 4 eksempler på verdien 10, blir B[arr[key]] = 4 til slutt
							  // Dette betyr at denne implementasjonen bare lagrer forekomster av hver verdi i stedet for å lagre den faktiske verdien i en 'bøtte'.
			arr[key] = -1;
		}

		int finalIndex = 0;
		for(int key = 0 ; key < arr.length ; key++ ){
			for(int x = 0 ; x < B[key] ; x++){
				arr[finalIndex++] = key;
				//Oblig3.printArray("",arr);
			}

		}

		return arr;
	}






	/*
		Algorithm SelectionSort(A):
		Input: An array A of n comparable elements, indexed from 1 to n 
		Output: An ordering of A so that its elements are in nondecreasing order


		for i ← 1 to n − 1 do
			// Find the index, s, of the smallest element in A[i..n].

			 s←i

			for j ← i + 1 to n do
				if A[j] < A[s] then 
					s←j

			if i != s then
				// Swap A[i] and A[s]
				t ← A[s];
				A[s] ← A[i];
				A[i] ← t;
		return A
		*/


	// Selection-Sort som spesifisert i oppskriften i boka. 
	public static int[] selectionSort(int [] arr){
		

		int s, temp;
		
		for(int i = 0; i < arr.length -1 ; i++){

			s = i;

			for(int j = i +1; j < arr.length ; j++){
				if(arr[j] < arr[s])
					s = j;
			}
			
			if( i != s) {
				temp = arr[s];
				arr[s] = arr[i];
				arr[i] = temp;
			}
			//Oblig3.printArray("iteration: ",arr);
			
		}


		return arr;
	}


}



