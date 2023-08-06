# Appchance :: Backend Spellbook

Hacks and project automation. Toolbelt for wizards and ninjas.

#
## Installation
Install package with pip

    pip install appchance

#
### Usage
1. Initialize and start new django application boosted by docker containers.
```
$ pip install appchance
$ dodo init
```

2. Add `doit.cfg` file in your project root directory with contents:
```
[GLOBAL]
backend=sqlite3
dep_file=.ddb.sql3
compose_cmd=docker-compose
dj_service=django
```


#
## Subpackages
Tools includes

- `dodos` = project automation
- `pickup` = pickup points for deliveries (DHL, Paczkomaty)
- `shop` = common models, serializers etc for django mcommerce

#
## Roadmap
Roadmap for future releases

* `0.1.0` = Project initialization
* `0.2.0` = Cookiecutter django-appchance
* `0.2.3` = Shop submodule improvements
* `0.2.5` = Dodo minor improvements
* `0.3.0` = Sections subpackage
* `0.4.0` = Dodo SSH
* `0.5.0` = Sentry integrations
* `0.6.0` = ELK integrations
