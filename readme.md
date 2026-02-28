# Korean Multiword Postpositions

This repository accompanies the paper "[A Curious Class of Adpositional Multiword Expressions in Korean](https://arxiv.org/abs/2602.16023)"
by Junghyun Min, Na-Rae Han, Jena D. Hwang, and Nathan Schneider.

`main.py` retrieves candidates for our proposed postpositional MWEs: PVCs from 
Korean Wikipedia, using `konlpy`'s `Mecab` morphology parser.

Compared to regular verbs, PVCs tend to be more frequent and more fossilized, occurring with smaller variants of josa and suffixes.

From the retrieved candidates, we manually review and propose that 15 are p-MWEs.


| Bound stem | Total Occ. | Adposition     | Main predicate? | Meaning         | Suffix forms with -hata inflections        | Homonyms                                                            |
|:-----------|:-----------|:---------------|:----------------|:----------------|:-------------------------------------------|:--------------------------------------------------------------------|
| 대 tay      | 272,022    | 에 ey           | FALSE           | about           | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye | 를 대하다 ul tayhata 'treat'                                            |
| 의 ui       | 170,110    | 에 ey           | FALSE           | by              | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye |                                                                     |
| 통 thong    | 122,731    | 를 lul          | FALSE           | via, through    | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye | 와 통하다 wa thonghata 'connect, flow'                                  |
| 위 wui      | 119,673    | 를 lul          | FALSE           | for             | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye | 를 위하다 lul wuihata 'care for'                                        |
| 인 in       | 85,339     | 로 lo           | FALSE           | due to          | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye |                                                                     |
| 관 kwan     | 63,819     | 에 ey           | FALSE           | about           | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye |                                                                     |
| 속 sok      | 38,378     | 에 ey           | TRUE*           | in              | -해 -hay,  -한 -han                          |                                                                     |
| 향 hyang    | 19,777     | 에 ey, 에게 eykey | TRUE*           | towards         | -해 -hay,  -한 -han                          |                                                                     |
| 비 pi       | 18,449     | 에 ey           | FALSE           | than            | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye | 와 비하다 wa pihata 'be comparable to'                                  |
| 불구 pwulkwu | 14,989     | 에도 eyto        | FALSE           | although        | -하고 -hako                                  | 불구되다 pwulkwu-toita^, 불구가 되다 pwulkwu-ka toita 'become crippled'^     |
| 비롯 piros   | 12,233     | 를 lul          | FALSE           | such as         | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye | 에서 비롯하다 eyse piros-hata, 에서 비롯되다 eyse piros-toita 'originates from' |
| 기 ki       | 4,839      | 를 lul          | TRUE*           | since           | -해 hay,  -한 -han                           |                                                                     |
| 반 pan      | 3,945      | 에 ey           | FALSE           | against, unlike | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye | 에(게) 반하다 ey(key) panhata 'fall for'                                 |
| 위시 wisi    | 135        | 를 lul          | FALSE           | such as         | -해 -hay, -한 -han, -해서 ey -hayse, -하여 -haye |                                                                     |

^Light verb constructions\
*Only possible as a connective verb in a serial verb construction as in (1)

(1)&nbsp;&nbsp;하늘을&emsp;&emsp;향해&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;날아가다\
&emsp;&emsp;hanul-ul&emsp;&nbsp;&nbsp;hyang-hay&nbsp;&nbsp;&emsp;&nbsp;&nbsp; nalakata\
&emsp;&emsp;sky-ACC&emsp;directing.conn&emsp;fly\
&emsp;&emsp;'fly towards the sky'