# nextbike_CGN


Der Leihfahrradanbieter "nextbike" bietet für seine jeweiligen Städte eine simple Schnittstelle (API) in Form einer aktuellen XML-Datei an. Diese besteht hauptsächlich aus verschiedenen Ortselementen, die mit Geodaten (Breiten- und Längengraden) versehen sind, sowie aus deren Kindelementen, die sich aus den gerade unbenutzten Fahrrädern an den jeweiligen Orten ergeben.

Mittels des Skripts "1_grab_xml.py" ist es möglich, für eine ausgewählte Stadt in einem gewünschten Zeitintervall (z.B. halbstündlich für 7 Tage) auf die jeweilige XML-Datei von der Schnittstelle zuzugreifen und diese mit dem aktuellen Zeitstempel abzuspeichern. 

Das zweite Skript "2_xml_to_csv.py" ermöglicht es, aus den gespeicherten XML-Dateien alle Fahrrad-Vorkommnisse mit ihren Informationen und der ID des zugeordneten Ortes (jedes Fahrrad hat potenziell mehrere Ort-IDs durch die Veränderung des Standortes über das Zeitintervall) sowie alle Ortsangaben mit ihren Informationen zu ziehen und diese in zwei separate CSV-Dateien zu packen. Zusätzlich werden die Geodaten der Ortsangaben in ungefähre Adressen umgewandelt.

Im dritten Skript "3_csv_to_sql_new.py" wird eine SQL-basierte (SQLite) Datenbank mit drei Tabellen für Fahrräder, Orte und Vorkommnisse (Verknüpfung Fahrräder und Orte) angelegt, in die die Daten der CSV-Dateien gespeist werden. 

Das vierte Skript "4_calculate_geodistances.py" ermöglicht die Abfrage der Datenbank nach einzelnen Fahrrädern und den jeweiligen Ortsangaben über das gewählte Zeitintervall. Durch die chronologische Abfolge der Ortsangaben für jedes Fahrrad erfolgt eine Distanzberechnung der Geodaten, sodass für jedes Fahrrad die im Zeitintervall zurückgelegte Distanz berechnet werden kann. Hieraus sind prinzipiell weitere Berechnungen möglich wie die durchschnittlich zurückgelegte Distanz der Fahrräder sowie die beliebtesten Fahrräder.


















