---
title: People
permalink: /people/
---

{% assign flora = site.people | where: "title", "Prof Flora Salim" %}
{% assign others = site.people | where_exp: "item", "item.title != 'Prof Flora Salim'" %}
{% assign others_sorted = others | sort: "name" %}
{% assign people_sorted = flora | concat: others_sorted %}

{% assign role_array = "academics|postdoc|visitingfellow|gradstudent|mphil|masterstudent|ugstudent|alumni" | split: "|" %}
{% for role in role_array %}

{% assign people_in_role = people_sorted | where: 'position', role %}

<!-- Skip section if there's nobody -->
{% if people_in_role.size == 0 %}
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
<h3>Master's Students</h3>
 {% elsif role == 'ugstudent' %}
<h3>Undergraduate & Honours Students</h3>
 {% elsif role == 'visitingfellow' %}
<h3>Visiting Fellows</h3>
 {% elsif role == 'alumni' %}
<h3>Alumni</h3>
{% endif %}
</div>

{% if role != 'alumni' %}
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

{% else %}

<br>

| Name                     | Former Position       | Where they went                                                  |
| ------------------------ | --------------------- | ---------------------------------------------------------------- |
| Yonchanok (Pro) Khaokaew | PhD Student & Postdoc | King Mongkut's University of Technology North Bangkok            |
| Imran Razzak             | Senior Lecturer       | Mohamed bin Zayed University of Artificial Intelligence (MBZUAI) |
| Matthew Low              | Honours               | Atlassian                                                        |
| Maodong Li               | Master's              | JD.com                                                           |
| Chenlu Ju                | Honours               |                                                                  |
| Jiaxin Liu               | Master's              |                                                                  |
| Shohreh Deldari          | Postdoc               | Bain & Company                                                   |
| Dhruv Agrawal            | Honours               |                                                                  |
| Hamada Rizk              | Visiting Fellow       | Osaka University                                                 |
| Luan Pham                | Visiting PhD Student  | Amazon United States                                             |
| Si Zuo                   | Visiting PhD Student  | Aalto University                                                 |
| Tianqi Tang              | Postdoc               | ByteDance Singapore                                              |
| Francis Zac dela Cruz    | Master's              | Freelancer.com                                                   |

{% endif %}
{% endfor %}

<hr>