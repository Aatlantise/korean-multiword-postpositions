# Korean Multiword Postpositions

This repository accompanies the paper "A Curious Class of Adpositional Multiword Expressions in Korean"
by Junghyun Min and Nathan Schneider.

`main.py` retrieves candidates for our proposed postpositional multiword expressions from 
Korean Wikipedia.

From the retrieved candidates, we manually review and propose that 18 are p-MWEs.


| Root | Total Occ. | Josa Co. | Suffix Co. | MWE Co | Nonverb. pred? | Dist. adp?               | Forms | Homonyms |
| :--- |:-----------|:---------|:-----------| :--- |:---------------|:-------------------------| :--- | :--- |
| 대 | 272,022    | 27       | 11         | 57 | TRUE           | about                    | 에 대해, 에 대한, 에 대해서, 에 대하여 | 을(를) 대하다* |
| 의 | 170,110    | 20       | 30         | 26 | TRUE           | by                       | 에 의해, 에 의한, 에 의해서, 에 의함, 에 의하여 | |
| 통 | 122,731    | 16       | 6          | 35 | TRUE           | via, through             | 를 통해, 를 통한, 를 통해서, 를 통함, 를 통하여 | 와 통하다* |
| 위 | 119,673    | 11       | 6          | 16 | TRUE           | for                      | 를 위해, 를 위한, 를 위해서, 를 위하여 | 를 위하다* |
| 인 | 85,339     | 15       | 5          | 21 | TRUE           | due to                   | 로 인해, 로 인한, 로 인해서, 로 인하여 | |
| 관 | 63,819     | 17       | 5          | 27 | TRUE           | about                    | 에 관해, 에 관한, 에 관해서, 에 관하여 | |
| 속 | 38,378     | 14       | 12         | 34 | FALSE          | in                       | 에 속하다* | |
| 향 | 19,777     | 10       | 6          | 32 | FALSE          | towards                  | 를 향하다*, 에게 향하다* | |
| 비 | 18,449     | 14       | 5          | 14 | TRUE           | than                     | 에 비해, 에 비한, 에 비해서, 에 비할, 에 비하여 | 와 비하다* |
| 불구 | 14,989     | 2        | 1          | 2 | TRUE           | although                 | 에도 불구하고 | 불구되다*, 불구가 되다* |
| 취 | 12,267     | 16       | 6          | 46 | FALSE          | on, under (the influence | 에 취하다* | 를 취하다*, 로 취하다* |
| 비롯 | 12,233     | 7        | 248        | 214 | TRUE           | such as                  | 를 비롯해, 를 비롯한, 를 비롯하여, | 에서 비롯하다*, 에서 비롯되다* |
| 기 | 4,839      | 14       | 11         | 35 | FALSE          | since                    | 를 기하여, 를 기해, 를 기함 | |
| 처 | 4,816      | 6        | 7          | 11 | FALSE          | in (the situation of)    | 에 처하다 (passive) * | 에 처하다* (active; to sentence) |
| 반 | 3,945      | 15       | 10         | 19 | TRUE           | against                  | against: 에 반한, 에 반하는, (의지)와 반해, (의지)와 반하여; unlike: 에 반하여, 에 반해 | 에(게) 반하다* (fall for) |
| 근거 | 2,255      | 5        | 13         | 14 | FALSE          | based on                 | 에 근거하다* | |
| 위시 | 135        | 2        | 2          | 2 | TRUE           | such as                  | 를 위시하여, 를 위시해 | |

Full table is available at https://georgetown1-my.sharepoint.com/:x:/g/personal/jm3743_georgetown_edu/IQCrP8s55cc3RpRpQJdzrEBTAZepvaj7keMPMOmJLiPuC-Q?e=jfJlNc.
