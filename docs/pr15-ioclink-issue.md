# PR #15: Problem mit IocLink-Tabelle

## Ursache

Der Pull Request #15 führte eine neue `IocLink`-Datenbanktabelle ein, um IOCs (Indicators of Compromise) mit mehreren Cases verknüpfen zu können. Die bestehende Datenbank verwendet jedoch einen anderen Ansatz: IOCs haben direkt eine `case_id`-Spalte in der `ioc`-Tabelle.

Die Datenbank-Migration `3715d4fac4de` (`add_link_between_case_and_ioc.py`) wurde im upstream IRIS-Projekt entwickelt, um genau den umgekehrten Weg zu gehen: von der `ioc_link`-Tabelle **weg** und hin zu `ioc.case_id`. PR #15 basierte auf einem Zwischenstand, der `ioc_link` noch verwendete.

## Fehlerbild

Beim Laden der IOCs in einem Case wurde folgender Fehler geworfen:

```
psycopg2.errors.UndefinedTable: relation "ioc_link" does not exist
```

Die `ioc_link`-Tabelle existiert nicht in der Datenbank, aber der Code versuchte, darauf zuzugreifen.

## Betroffene Bereiche

Folgende Funktionen mussten von `IocLink` auf `Ioc.case_id` zurückgesetzt werden:

| Datei | Funktionen |
|---|---|
| `app/datamgmt/case/case_iocs_db.py` | `get_iocs`, `get_ioc`, `delete_ioc`, `get_detailed_iocs`, `get_ioc_links`, `add_ioc`, `case_iocs_db_exists`, `get_ioc_by_value`, `get_filtered_iocs` |
| `app/datamgmt/manage/manage_cases_db.py` | `_delete_iocs` (Case-Löschbereinigung) |
| `app/datamgmt/case/case_artifacts_db.py` | `escalate_artifact` |
| `app/business/comments.py` | `comments_create_for_ioc` |
| `app/business/iocs.py` | `iocs_delete` (Signatur angepasst) |
| `app/schema/marshables.py` | `get_link` in `IocSchemaForAPIV2` und `IocSchema` |
| `app/blueprints/rest/case/case_ioc_routes.py` | `case_list_ioc` (Aufruf von `get_ioc_links`) |
| `app/blueprints/rest/v2/case_routes/iocs.py` | `get_ioc_linked_cases` (Linked-Cases-Endpoint) |

## Architektur der alten Lösung

IOCs gehören zu genau einem Case (`Ioc.case_id`). Um IOCs zu finden, die in anderen Cases vorkommen, wird nach IOCs mit dem **gleichen Wert und Typ** in anderen Cases gesucht:

```python
def get_ioc_links(ioc_id, user_search_limitations):
    ioc = Ioc.query.filter(Ioc.ioc_id == ioc_id).first()
    related_iocs = Ioc.query.filter(
        Ioc.ioc_value == ioc.ioc_value,
        Ioc.ioc_type_id == ioc.ioc_type_id,
        Ioc.ioc_id != ioc_id,
        search_condition
    ).join(Ioc.case).all()
    return related_iocs
```

## Ausblick

Soll die `ioc_link`-Tabelle doch eingeführt werden, müsste:

1. Eine neue Alembic-Migration erstellt werden, die die Tabelle anlegt
2. Bestehende IOCs in `ioc_link`-Einträge migriert werden
3. Alle zurückgesetzten Funktionen wieder auf `IocLink` umgestellt werden
