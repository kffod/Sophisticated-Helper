## AS400/IBM i Cheat Sheet

**I.  Connections & Navigation**

* **Telnet/SSH:** Connect via telnet or ssh to the system's IP address.
* **STRSSESSION:** Start a 5250 session (emulator needed).
* **WRKACTJOB:** View active jobs.
* **WRKOBJLCK:** View object locks.
* **GO CMD:** Navigate to commands (e.g., `GO DSPPGM`).
* **F4 (Prompt):** Get help and parameter options.
* **F10 (Return):** Execute command.
* **F11 (Menu):** Access menus if available.
* **F12 (Cancel):** Cancel operation.


**II.  Object Management**

* **CRTLIB:** Create library.  `CRTLIB LIB(MYLIB)`
* **CRTPGM:** Create program. `CRTPGM PGM(MYPGM) SRCFILE(MYFILE)`
* **CRTSRCPF:** Create source physical file. `CRTSRCPF FILE(MYFILE) SRCSTMF(*SRC)`
* **CRTPF:** Create physical file. `CRTPF FILE(MYFILE) RCDLEN(100)`
* **DSPLIB:** Display libraries.
* **DSPOBJD:** Display object description. `DSPOBJD OBJ(MYPGM) OBJTYPE(*PGM)`
* **RMVLIB:** Remove library. `RMVLIB LIB(MYLIB)`
* **RMVOBJ:** Remove object. `RMVOBJ OBJ(MYPGM) OBJTYPE(*PGM)`


**III.  Data Manipulation (SQL)**

* **STRSQL:** Start SQL session.
* **SELECT * FROM MYLIB/MYFILE:** Select all columns from a file.
* **INSERT INTO MYFILE VALUES (val1, val2):** Insert a row.
* **UPDATE MYFILE SET col1 = val WHERE col2 = val2:** Update a row.
* **DELETE FROM MYFILE WHERE col1 = val:** Delete a row.
* **COMMIT:** Save changes.
* **ROLLBACK:** Undo changes.


**IV.  Job Management**

* **ENDJOB:** End current job.
* **WRKJOB:** Work with jobs.
* **WRKJOB SBMJOB(*JOB):** Manage specific job.
* **QSYSOPR:** System operator message queue.


**V.  Basic Commands**

* **CHGVAR:** Change variable. `CHGVAR VAR(&MYVAR) VALUE('HELLO')`
* **DSPVAR:** Display variable. `DSPVAR VAR(&MYVAR)`
* **OUTQ:** Output queue for spooled files.
* **DSPJOB:** Display job information.


**VI.  Important Considerations**

* Case sensitivity matters.
* Libraries are crucial for object organization.
* Use descriptive object names.
* Backup regularly.
* Consult IBM documentation for detailed information.


This is a *concise* overview.  Full command syntax and options require extensive IBM i documentation.
