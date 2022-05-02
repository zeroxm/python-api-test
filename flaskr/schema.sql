DO
$do$
begin
	IF EXISTS (SELECT FROM information_schema.tables
				WHERE  table_schema = 'public'
				AND   table_name   = 'post') then
		drop table post;
	END IF;
	IF EXISTS (SELECT FROM information_schema.tables
				WHERE  table_schema = 'public'
				AND   table_name   = 'usuario') then
		drop table usuario;
	END IF;

	CREATE TABLE usuario (
	  id serial PRIMARY KEY,
	  username TEXT UNIQUE NOT NULL,
	  password TEXT NOT NULL
	);
	
	CREATE TABLE post (
	  id serial PRIMARY KEY,
	  author_id INTEGER NOT NULL,
	  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  title TEXT NOT NULL,
	  body TEXT NOT NULL,
	  FOREIGN KEY (author_id) REFERENCES usuario (id)
	);
END
$do$