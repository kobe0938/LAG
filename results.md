# RAG v.s. LAG

Total docs: 30 (3 positive, 27 negative)

RAG:

| Rank | Score  | Label | Document (first 80 chars) |
|------|--------|-------|---------------------------|
| 1    | 0.8429 | NEG X | Oct 5, 2022 ... The 2022 Nobel Prize in Chemistry has been awarded to three scie... |
| 2    | 0.7114 | NEG X | Oct 5, 2022 ... The 2022 Nobel Prize for Chemistry has been jointly awarded to t... |
| 3    | 0.7000 | NEG X | A 1986 DNA model used by Aziz Sancar, who was awarded the 2015 Nobel Prize in Ch... |
| 4    | 0.6860 | NEG X | © Nobel Prize Outreach. Photo: Stefan Bladh  Prize share: 1/3  © Nobel Prize Out... |
| 5    | 0.6750 | NEG X | The Nobel committee said in a statement that "click chemistry and bioorthogonal... |
| 6    | 0.6593 | NEG X | Bioorthogonal reactions are used widely to investigate vital processes in cells,... |
| 7    | 0.6454 | NEG X | Oct 5, 2022 ... Barry Sharpless, PhD, has been awarded the 2022 Nobel Prize in C... |
| 8    | 0.6373 | NEG X | Oct 5, 2022 ... Comments • 52 · Stanford's Carolyn Bertozzi, 2022 Nobel Laureate... |
| 9    | 0.6345 | POS Y | Advertisement Supported by Carolyn R. Bertozzi, Morten Meldal and K. Barry Sharp... |
| 10   | 0.6320 | NEG X | Did you know that there is no public list of the current year's nominees for the... |
| 11   | 0.6282 | NEG X | Learn more about Svante Arrhenius, who first made the connection between carbon... |
| 12   | 0.6246 | POS Y | The Nobel Prize in Chemistry 2022 was awarded to Carolyn R. Bertozzi, Morten Mel... |
| 13   | 0.6222 | NEG X | In the ten years leading up to 2012, only four prizes were awarded for work stri... |
| 14   | 0.6153 | POS Y | Sharpless awarded his second Nobel Prize in Chemistry–one of only two chemists t... |
| 15   | 0.5943 | NEG X | As of 2022 only eight women had won the prize: Marie Curie, her daughter Irène J... |
| 16   | 0.5714 | NEG X | Sherwood Rowland and Mario Molina at work, January 1975. University of Californi... |
| 17   | 0.5703 | NEG X | Nobel laureates receive a diploma directly from the hands of the King of Sweden.... |
| 18   | 0.5251 | NEG X | As a downside of this approach, not all scientists live long enough for their wo... |
| 19   | 0.5225 | NEG X | Wanting to make amends, he did what no man of such wealth had done before … On 1... |
| 20   | 0.5155 | NEG X | "This has really opened up an immense amount of new space for scientists to stud... |
| 21   | 0.5153 | NEG X | Bertozzi also became the eighth woman to be awarded the chemistry prize, the lat... |
| 22   | 0.5098 | NEG X | citation needed]  The Nobel Laureates in chemistry are selected by a committee t... |
| 23   | 0.4901 | NEG X | This platform has transformed how scientists approach drug discovery, bioimaging... |
| 24   | 0.4839 | NEG X | The members of the Norwegian Nobel Committee that were to award the Peace Prize... |
| 25   | 0.4729 | NEG X | From Stockholm, the Royal Swedish Academy of Sciences confers the prizes for phy... |
| 26   | 0.4615 | NEG X | "What's unique about click chemistry is that the two reagents, in the presence o... |
| 27   | 0.4607 | NEG X | "Carolyn Bertozzi had a profound impact at Berkeley Lab, not only through her br... |
| 28   | 0.4560 | NEG X | Their buckles easily snapped together and wouldn't link onto anything they shoul... |
| 29   | 0.4448 | NEG X | Winter for harnessing the power of evolution to produce novel, beneficial enzyme... |
| 30   | 0.4415 | NEG X | The Nobel Prize in Physiology or Medicine 2022 was awarded to Svante Pääbo "for... |

LAG:

| Rank | P(YES) | Token | Label | Document (first 80 chars) |
|------|--------|-------|-------|---------------------------|
| 1    | 1.0000 | YES   | NEG X | Oct 5, 2022 ... Barry Sharpless, PhD, has been awarded the 2022 Nobel Prize... |
| 2    | 1.0000 | YES   | POS Y | Advertisement Supported by Carolyn R. Bertozzi, Morten Meldal and K. Barry... |
| 3    | 1.0000 | YES   | NEG X | Oct 5, 2022 ... The 2022 Nobel Prize for Chemistry has been jointly awarded... |
| 4    | 1.0000 | YES   | POS Y | Sharpless awarded his second Nobel Prize in Chemistry–one of only two chemi... |
| 5    | 1.0000 | YES   | NEG X | Bioorthogonal reactions are used widely to investigate vital processes in c... |
| 6    | 1.0000 | YES   | POS Y | The Nobel Prize in Chemistry 2022 was awarded to Carolyn R. Bertozzi, Morte... |
| 7    | 0.9994 | YES   | NEG X | Oct 5, 2022 ... Comments • 52 · Stanford's Carolyn Bertozzi, 2022 Nobel Lau... |
| 8    | 0.8808 | YES   | NEG X | "This has really opened up an immense amount of new space for scientists to... |
| 9    | 0.0000 | NO    | NEG X | The Nobel Prize in Physiology or Medicine 2022 was awarded to Svante Pääbo... |
| 10   | 0.0000 | NO    | NEG X | This platform has transformed how scientists approach drug discovery, bioim... |
| 11   | 0.0000 | NO    | NEG X | A 1986 DNA model used by Aziz Sancar, who was awarded the 2015 Nobel Prize... |
| 12   | 0.0000 | NO    | NEG X | Did you know that there is no public list of the current year's nominees fo... |
| 13   | 0.0000 | NO    | NEG X | Learn more about Svante Arrhenius, who first made the connection between ca... |
| 14   | 0.0000 | NO    | NEG X | Sherwood Rowland and Mario Molina at work, January 1975. University of Cali... |
| 15   | 0.0000 | NO    | NEG X | Nobel laureates receive a diploma directly from the hands of the King of Sw... |
| 16   | 0.0000 | NO    | NEG X | As a downside of this approach, not all scientists live long enough for the... |
| 17   | 0.0000 | NO    | NEG X | Wanting to make amends, he did what no man of such wealth had done before …... |
| 18   | 0.0000 | NO    | NEG X | Bertozzi also became the eighth woman to be awarded the chemistry prize, th... |
| 19   | 0.0000 | NO    | NEG X | citation needed]  The Nobel Laureates in chemistry are selected by a commit... |
| 20   | 0.0000 | NO    | NEG X | The members of the Norwegian Nobel Committee that were to award the Peace P... |
| 21   | 0.0000 | NO    | NEG X | From Stockholm, the Royal Swedish Academy of Sciences confers the prizes fo... |
| 22   | 0.0000 | NO    | NEG X | Winter for harnessing the power of evolution to produce novel, beneficial e... |
| 23   | 0.0000 | NO    | NEG X | As of 2022 only eight women had won the prize: Marie Curie, her daughter Ir... |
| 24   | 0.0000 | NO    | NEG X | "What's unique about click chemistry is that the two reagents, in the prese... |
| 25   | 0.0000 | NO    | NEG X | Their buckles easily snapped together and wouldn't link onto anything they... |
| 26   | 0.0000 | NO    | NEG X | Oct 5, 2022 ... The 2022 Nobel Prize in Chemistry has been awarded to three... |
| 27   | 0.0000 | NO    | NEG X | The Nobel committee said in a statement that "click chemistry and bioorthog... |
| 28   | 0.0000 | NO    | NEG X | "Carolyn Bertozzi had a profound impact at Berkeley Lab, not only through h... |
| 29   | 0.0000 | NO    | NEG X | © Nobel Prize Outreach. Photo: Stefan Bladh  Prize share: 1/3  © Nobel Priz... |
| 30   | 0.0000 | NO    | NEG X | In the ten years leading up to 2012, only four prizes were awarded for work... |
