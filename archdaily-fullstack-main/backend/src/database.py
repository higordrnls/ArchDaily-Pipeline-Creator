import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="arquitetura_db",
        user="dev_user",
        password="dev_password"
    )

def inicializar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticias (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            data_publicacao DATE NOT NULL,
            link TEXT UNIQUE NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticia_tags (
            noticia_id INT REFERENCES noticias(id) ON DELETE CASCADE,
            tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (noticia_id, tag_id)
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Banco de dados e tabelas prontos!")

def salvar_noticias_no_banco(noticias):
    if not noticias:
        print("⚠️ Nenhuma notícia para salvar.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    salvos = 0
    for noti in noticias:
        try:
            cursor.execute("""
                INSERT INTO noticias (titulo, data_publicacao, link)
                VALUES (%s, %s, %s)
                ON CONFLICT (link) DO NOTHING
                RETURNING id;
            """, (noti["titulo"], noti["data"], noti["link"]))
            resultado = cursor.fetchone()
            if resultado:
                noticia_id = resultado[0]
                salvos += 1
                for tag_nome in noti["tags"]:
                    cursor.execute("""
                        INSERT INTO tags (nome)
                        VALUES (%s)
                        ON CONFLICT (nome) DO UPDATE SET nome = EXCLUDED.nome
                        RETURNING id;
                    """, (tag_nome.lower().strip(),))
                    tag_id = cursor.fetchone()[0]
                    cursor.execute("""
                        INSERT INTO noticia_tags (noticia_id, tag_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (noticia_id, tag_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"❌ Erro ao salvar: {e}")
    cursor.close()
    conn.close()
    print(f"💾 Banco atualizado! {salvos} novas notícias salvas.")