# Semantic FAQ Assistant

## Setup instructions
--create env
python -m venv venv

---pwshell/activate env
venv\Scripts\activate

pip install -r requirements.txt

### PostgreSQL setup
1. Install PostgreSQL (version 17 on my local/device)
```winget install PostgreSQL.PostgreSQL```
2. pgvector extension is required (installed via cmd)

# cmd
```
set PGROOT=C:\Program Files\PostgreSQL\17
set PATH=C:\Program Files\PostgreSQL\17\bin;%PATH%
set PG_CONFIG=C:\Program Files\PostgreSQL\17\bin\pg_config

# Initialize Visual Studio Build Tools
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

# Build and install pgvector
cd C:\temp\pgvector\pgvector-0.5.1
nmake /f Makefile.win
nmake /f Makefile.win install
```



