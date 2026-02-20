---
title: People
permalink: /people/
---

{% assign flora = site.people | where: "title", "Prof Flora Salim" %}
{% assign others = site.people | where_exp: "item", "item.title != 'Prof Flora Salim'" %}
{% assign others_sorted = others | sort: "name" %}
{% assign people_sorted = flora | concat: others_sorted %}

{% assign role_array = "academics|postdoc|visitingfellow|softwareengineer|gradstudent|mphil|masterstudent|ugstudent|visitor|alumni|former_visitors" | split: "|" %}
{% for role in role_array %}

{% assign people_in_role = people_sorted | where: 'position', role %}

<!-- Skip section if there's nobody -->
{% if people_in_role.size == 0 and role != 'alumni' and role != 'former_visitors' %}
  {% continue %}
{% endif %}

<div class="pos_header">
{% if role == 'postdoc' %}
<h3>Postdoc, Research Fellow & Research Associates</h3>
 {% elsif role == 'academics' %}
<h3>Academics</h3>
 {% elsif role == 'gradstudent' %}
<h3>PhD Students</h3>
 {% elsif role == 'mphil' %}
<h3>MPhil Students</h3>
 {% elsif role == 'masterstudent' %}
<h3>Master Thesis Students</h3>
 {% elsif role == 'ugstudent' %}
<h3>Undergraduate & Honours Students</h3>
 {% elsif role == 'visitingfellow' %}
<h3>Visiting Fellows</h3>
 {% elsif role == 'softwareengineer' %}
<h3>Software Engineers</h3>
 {% elsif role == 'alumni' %}
<h3>Alumni</h3>
 {% elsif role == 'visitor' %}
<h3>Current Visitors</h3>
 {% elsif role == 'former_visitors' %}
<h3>Past Visiting Fellows & Students</h3>
{% endif %}
</div>

{% if role != 'alumni' and role != 'former_visitors' %}
<div class="content list people">
  {% for profile in people_sorted %}
    {% if profile.position contains role %}
      <div class="list-item-people">
        <p class="list-post-title">
          {% if profile.avatar %}
            <a href="{{ site.baseurl }}{{ profile.url }}"><img class="profile-thumbnail" src="{{site.baseurl}}/images/people/{{profile.avatar}}"></a>
          {% else %}
            <a href="{{ site.baseurl }}{{ profile.url }}"><img class="profile-thumbnail" src="{{site.baseurl}}/images/people/facebook-Storm-Trooper.png"></a>
          {% endif %}
          <a class="name" href="{{ site.baseurl }}{{ profile.url }}">{{ profile.name }}</a>
        </p>
      </div>    
    {% endif %}
  {% endfor %}
</div>
<hr>

{% elsif role == 'former_visitors' %}

<br>

| Name            | Where they came from                   |
| --------------- | -------------------------------------- |
| Marco Bustaffa  | University of Padova                   |
| Zefan Sramek    | University of Tokyo                    |
| Hamada Rizk     | Osaka University                       |
| Luan Pham       | RMIT                                   |
| Si Zuo          | Aalto University                       |
| Lorenzo Lamazzi | University of Modena and Reggio Emilia |

{% elsif role == 'alumni' %}

<br>

<!-- | Declan Curran | MPhil Student |                                | -->
<!-- | Freya Stevens | Master Thesis |   | -->
<!-- | Hada Melino | Master Thesis |     | -->
<!-- | Xiheng Chen | Master Thesis |   | -->
<!-- | Quoc (Peter) Pham | Honours |   | -->
<!-- | Yunzhi Liu | Master Thesis |  | -->
<!-- | Caike Lin                  | Master Thesis         |                                                                  | -->
<!-- | Bohan Zhang                | Honours               |                                                                  | -->
<!-- | Hongkun Wang               | Honours               |                                                                  | -->
<!-- | Shiqi Su                   | Master Thesis         |                                                                  | -->
<!-- | Jiaxin Liu                 | Master Thesis         |                                                                  | -->

| Name                       | Former Position       | Where they went                                                  |
| -------------------------- | --------------------- | ---------------------------------------------------------------- |
| Arian Prabowo              | Postdoc               | Oracle                                                           |
| Ji Miao                    | Master Thesis         | JD.com                                                           |
| Emma Casolin               | Honours               | AWS                                                              |
| Xiaoqian Hu                | Master Thesis         | University of Queensland                                         |
| Haley Stone                | Postdoc               | University of Glasgow                                            |
| Yue Tan                    | Postdoc               | Ninja AI                                                         |
| Arthur Chen                | MPhil Student         | UNSW                                                             |
| Yonchanok (Pro) Khaokaew   | PhD Student & Postdoc | King Mongkut's University of Technology North Bangkok            |
| Imran Razzak               | Senior Lecturer       | Mohamed bin Zayed University of Artificial Intelligence (MBZUAI) |
| Matthew Low                | Honours               | Atlassian                                                        |
| Maodong Li                 | Master Thesis         | JD.com                                                           |
| Shohreh Deldari            | Postdoc               | Bain & Company                                                   |
| Dhruv Agrawal              | Honours               | Citadel Securities                                               |
| Tianqi Tang                | Postdoc               | ByteDance Singapore                                              |
| Francis Zac dela Cruz      | Master Thesis         | Dataro                                                           |
| Thuc Hanh (Grace) Nguyen   | Master Thesis         | Ericsson                                                         |
| Justin Luong               | Honours               | Adora                                                            |
| ***University of Kassel*** |
| Judith Heinisch            | PhD Student           | University of Kassel                                             |
| ***Flinders University***  |
| Lorenzo Yuxi Liu           | PhD Student           | University of Florida                                            |
| ***RMIT***                 |
| Hiruni Kegalle             | PhD Student           | University of Melbourne                                          |
| Yufan Kang                 | PhD Student           | Monash University                                                |
| Futoon Abu Shaqra          | PhD Student           | RMIT                                                             |
| Sichen Zhao                | PhD Student           | An energy company in China                                       |
| Kai Qin                    | PhD Student           | Data Engineering Lead at an AI Startup                           |
| Ali Hamdi Ali              | PhD Student           | MSA University, Egypt                                            |
| Shakila Khan Rumi          | PhD Student           | Australian Institute of Health and Welfare                       |
| Jonathan Liono             | PhD Student           | tiket.com                                                        |
| Hui Song                   | PhD Student           | Hangzhou Dianzi University                                       |
| Saiedur Rahaman            | PhD Student           | CQU                                                              |
| Irvan Bastian Arief        | PhD Student           | tiket.com                                                        |
| Wei Shao                   | PhD Student           | Data61                                                           |
| Amin Sadri                 | PhD Student           | ANZ                                                              |

<hr>

{% endif %}
{% endfor %}

<hr>