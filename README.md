# Kasiski
#### Video Demo:  [link to video demo](https://youtu.be/k21AIioce4U)
#### Try a [web-based version](https://kuunoDeRuyter.github.io/Kasiski/) live (converted from Python by Claude)
#### Description:

In a way, this project seeks to pick up where [CS50 problem set 2](https://cs50.harvard.edu/x/psets/2/) left off. More specifically, it is meant to offer the user a way to explore how variations in key and message length can affect the likelihood of cryptanalyzing a message encrypted using a Vigenère square, also known as a _tabula recta_. (Spoiler: ***Short messages are harder to crack*** because you have less data to analyze. Moreover, ***long encryption keys also make decryption more difficult*** because decryption methods rely heavily on detecting repetitions in the encrypted message. The longer a key is, the less often it repeats.)
```
                    short message      long message
short key     │  usually works        almost always works
long key      │  likely fails         often works, sometimes fails
```
As encryption methods go, [Caesar](https://cs50.harvard.edu/x/psets/2/caesar/) is among the easiest to beat. This is due to the fact that, when it's enciphered, each plaintext letter in the message is _always changed to the same ciphertext letter_. (With a Caesar shift of one, for example, every **A** would become a **B**, every **B** would become a **C**, and so on.) The obvious problem with this _monoalphabetic_ system is its direct vulnerability to [letter-frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis). (Or, failing this, a highly determined cryptanalyst could test the message against all 26 possible shifts while, after each shift, checking to see if the result is intelligible.)\
As long ago as the 16th century, cryptographers had created an alternative encipherment system that seemed to address the intrinsic weakness of the Caesar shift. This new approach eventually became known as the _Vigenère Cipher_ (pronounced 'vee-zhuh-NAIR'). According to [Encyclopedia Britannica](https://www.britannica.com/topic/Vigenere-cipher), for centuries, this cipher was mistakenly attributed to French diplomat Blaise de Vigenère instead of its true author, Italian cryptologist Giovan Battista Bellaso. Like the ciphers seen in both "Caesar" and ["Substitution"](https://cs50.harvard.edu/x/psets/2/substitution/), Vigenère is a _substitution cipher_ in which each letter of a message is replaced by another letter. The key difference, however, is that the Vigenère cipher employs a _polyalphabetic_ substitution scheme. This means that, in a message, each plaintext letter will usually _not_ be enciphered as the same letter each time it appears. While this represents a major improvement over the Caesar shift, the result is still far from perfect, as Friedrich Kasiski discovered.
#### square.py
At runtime, the program first creates and exports a Vigenère square to a text file.
1. The `alpha` variable contains the English alphabet in uppercase.
2. The `square` variable is a dictionary comprehension with tuples `(key_letter, plain_letter)` serving as keys while the values (the cipher letters) are defined as `(i + j) % 26`. As an example, `square[('B', 'T')]` would evaluate to **U** because `B=1, T=19, (1 + 19) % 26 = 20` and `alpha[20] = U`.
3. `Build_vigenere_square_text()` formats the `square` dictionary as a human-readable Vigenère square. The row headers (in column 1) represent key letters while column headers (row 1) represent plaintext letters. Spaces are inserted between characters for easier readability.
4. Finally, `export_vigenere_square()`, which was initially called by `main.py`, executes. This function calls `build_vigenere_square_text()`, creates a filepath for `vigenere_square.txt`, and exports the file. `Main.py` then prints a confirmation.
#### get_input.py
Next, `main.py` calls `get_message()` from the `get_input.py` file.
1. The program prompts the user to submit plaintext as well as an encryption keyword. For the message, the user may manually enter text or choose a snippet from `readability_text_samples.txt`. After successful validation, the plaintext is stored under the `raw` variable. (Note that the text snippets were obtained from books found at [Project Gutenberg](https://www.gutenberg.org/).)
2. The constant `MIN_MESSAGE_LENGTH` sets a requirement that messages contain at least 100 letters. (Details in _Design Choices_ below.) Using a regular expression, the `clean_message()` function strips all non-letters. This ensures the message only contains characters the cipher can work with.
3. Finally, `get_key()` uses the `.isalpha` method to ensure the keyword contains only letters while `MIN_KEY_LENGTH` sets 4 as the minimum length.
#### encrypt (main.py)
Now, `main.py` calls the `encrypt()` function, which is located at the top of the `main.py` file.
1. The plaintext message and key get passed to the function.
2. The `encrypted` variable collects the enciphered outputs while `key_index` keeps track of the current key letter.
3. Next, inside a `for` loop, variables `msg_pos` and `key_pos` convert the current plaintext letter as well as the current key letter to their respective numeric positions in `alpha`, which contains the English alphabet.
4. The `encrypted_pos` variable shows how Vigenère encipherment actually works. It finds the index of the enciphered letter by adding together the current plaintext index and the current key-letter index modulo 26, `encrypted_pos = (msg_pos + key_pos) % 26`.
5. Then, the function `appends` the corresponding letter to the `encrypted` list value. After that, `key_index` increments.
6. Once the `for` loop has iterated through the entire message, the newly enciphered text is returned to the `ciphertext` variable, which is printed to the screen.

Now it's time to start breaking the code. The method for doing so begins with seeking the length of the key used to encipher the message. This method is attributed to [Friedrich Wilhelm Kasiski](https://en.wikipedia.org/wiki/Friedrich_Kasiski), a retired Prussian army officer who published it in 1863.

- The first step in the Kasiski method is to look for sets of repeating characters within the ciphertext. (To minimize noise in the results, the repeating sets must be at least 3 letters long.)
- The next step is to count the number of letters separating the repeated letters. (For example, in 'UOAKT***AKL***UDDKT***AKL***UII', the distance between the two `AKL`s would be counted as 8.)
  - The underlying idea is that the same plaintext fragment ('the', for example) could align with the same part of the key at two different positions. This would produce identical ciphertext.
  - Since the Vigenère cipher repeats its key, this would mean that the length of the key would divide evenly into the number of letters separating these matching segments. So, in the preceding `AKL` example, the key length could be either 8 or 4. (Shorter lengths are not considered due to the unlikelihood of anyone choosing a key that is just 1 or 2 letters long.)
#### get_key_length.py
`Main.py` starts the decryption process by accessing the `get_key_length.py` file and calling the `print_kasiski_table()` function found therein.
1. `Print_kasiski_table()` immediately passes `ciphertext` to `find_repeat_sequences()`, which slides a 3-character window across the ciphertext and records every position where each trigram appears. It returns only the trigrams that appear **more than once**. These repeated sequences might offer a foothold for decryption.
2. `Main.py` then calls `estimate_key_length(ciphertext)` which:\
   a. Also calls `find_repeat_sequences()` to get all repeated trigrams and their positions.\
   b. For each repeated trigram, iterates over **consecutive pairs** of positions and computes the distance between them.\
   c. Factors that distance, keeping only factors in the range `[MIN_KEY_LENGTH, max_candidate]` (between 4 and half the message length). This filters out noise such as 2 and 3.\
   d. Tallies all candidate factors in a `Counter`.\
   e. Returns the **most common factor** — the estimated key length.\
   f. If no repeated sequences are found, it returns `1` (unknown).
#### get_key.py
Assuming the correct key length was found, it's now time to recover the key itself. `Main.py` accesses the `get_key.py` module and calls `split_into_groups()`.
1. The `split_into_groups()` function has two parameters: `ciphertext` and `key_length`. The function initializes the `groups` variable containing a list of empty strings equal in number to `key_length`. To clarify, if `key_length` = 4, then `groups` would at first contain `['', '', '', '']`.
2. Next, the function organizes the ciphertext by position modulo the key length. So if the key length is 4, the result would follow the pattern:
   - **Group 0**: positions 0, 4, 8, 12, …
   - **Group 1**: positions 1, 5, 9, 13, …
   - **Group 2**: positions 2, 6, 10, 14, …
   - **Group 3**: positions 3, 7, 11, 15, …
3. Each group was shifted by a single key letter so, in effect, all characters in each group were encrypted by a single Caesar shift. This makes each group potentially vulnerable to [frequency analysis](https://blogs.sas.com/content/iml/2014/09/19/frequency-of-letters.html).
4. Basically, `recover_key_letter()` uses `chi_squared_score()` as a tool to determine, with mathematical rigor, which of the 26 possible Caesar shifts causes each group's letter-usage pattern to most closely resemble [that of English](https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html). (I had never heard of the chi-squared test before this. That was all Claude.)
5. If all goes according to plan, the correct key is recovered and stored in the `recovered_key` variable in `main.py`. The recovered key and plaintext message, after being decrypted with the key, are then printed to screen.
6. If not everything worked perfectly, information on any "partial match" is provided.
#### Design Choices
- Once I noticed that this program was, at times, outputting a lot of data to the terminal, I decided to also export the analytic results to a plain text file (called `session_output.txt`) to make reviewing the data easier.
- Short messages are harder to decrypt than long ones. That is why plaintext messages must contain at least 100 letters. (Extremely short messages would fail to decrypt too often.) To spare the user the hassle of coming up with a long-ish message on the spot, the user may press the Enter key and select from among 4 copyright-free text samples arranged in order of increasing length. The first 3 samples are from CS50's readability problem. The fourth is from the novel _Dracula_.
- Also on the topic of message input, during a walkthrough of the code, I noticed that I had `samples = load_samples()` as the first line inside the `get_message()` function in `get_input.py`. Realizing that it made little sense to load the text samples whether they were needed or not, I moved `load_samples()` inside the function's while loop. That way, the text samples load only after the user indicates that s/he wants to use a text sample by pressing Enter at the message prompt:
```
    while True:
        raw = input("Message: ").strip()
        if raw == "":
            samples = load_samples()
```
