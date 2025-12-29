# Korean Multiword Postpositions

This repository accompanies the paper "A Curious Class of Adpositional Multiword Expressions in Korean"
by Junghyun Min and Nathan Schneider.

`main.py` retrieves canddates for our proposed postpositional light-verb based constructions (PLVCs) from 
Korean Wikipedia, based on frequency, fossilization, and human input.

From the retrieved candidates, we manually review and determine that 16 are PLVCs.

We each per our proposed taxonomy following the degree to which they are fossilized.


| PLVC                                            | Meaning | Freq/100 | Foss. |
|-------------------------------------------------| --- | --- | --- |
| **Fossilized PLVCs**                            ||||
| 에 대한 ey tayhan                                  | regarding, about | 98 | 0.86 |
| 에 의한 ey yihan                                   | by, according to | 53 | 0.90 |
| 에 관한 ey kwanhan                                 | regarding, about | 23 | 0.67 |
| 을 비롯한 ul pilos'han                              | such as | 12 | 0.80 |
| 을 위시한 ul uisihan                                | such as | 0.7 | 0.59 |
| **Lexicalized PLVCs with Limited Productivity** |  |  |  |
| 에 반해 ey panhay†                                 | unlike | 18 | 0.04 |
| 에 처한 ey chehan                                  | in (the situation of) | 5 | 0.13 |
| 에 취한 ey chuihan                                 | on, under (the influence of) | 2 | 0.33 |
| **PLVCs with productive light verb *hata***     |  |  |  |
| 을 위한 ul wihan                                   | for (the purpose, sake of) | 109 | 0.33 |
| 로 인한 lo inhan                                   | because of | 45 | 0.32 |
| 을 통한 ul thonghan                                | via, through | 39 | 0.94 |
| 에 속한 ey sok'han                                 | in (membership) | 27 | 0.11 |
| 에 비해 ey pihay                                   | than (comparative) | 18 | 0.37 |
| 에 반한 ey panhan†                                 | against | 18 | 0.04 |
| 을 향한 ul hyanghan                                | towards, directed to | 11 | 0.33 |
| 에 근거한 ey kunkehan                               | based on | 5 | 0.20 |

---

> **Notes:** > † *에 반한 ey panhan ‘against’ and 에 반해 ey panhay ‘unlike’ share the same root and statistics.*

---