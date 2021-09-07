	CREATE FUNCTION new_voter(index INT,name VARCHAR,surname VARCHAR) RETURNS TEXT
	AS $$
	BEGIN
		IF EXISTS (SELECT 1 FROM voter CROSS JOIN users WHERE index_number = index AND login = CAST(index AS VARCHAR)) THEN
		RETURN 'Voter with this index number is already registered';
		END IF;
		
		INSERT INTO voter VALUES (index,name,surname);
		INSERT INTO users VALUES (index,'voter','voter');
		RETURN 'Voter added successfully';

	END
	$$ LANGUAGE plpgsql;
 

	CREATE FUNCTION new_election(election_name VARCHAR, num_positions INTEGER, nomination_deadline DATE,begin_date  DATE,end_date  DATE)
	RETURNS TEXT
	AS $$
	BEGIN
		IF EXISTS (SELECT 1 FROM election WHERE name = election_name) THEN
		RETURN 'Already registered election with this name';
		END IF;
		
		IF nomination_deadline > begin_date THEN
		RETURN 'Nomination deadline must be before the start of the election';
		END IF;
		
		IF begin_date > end_date THEN
		RETURN 'The election must begin before it ends...';
		END IF;
		
		IF num_positions <1 THEN
		RETURN 'Number of positions must be a positive number';
		END IF;
	
		INSERT INTO election VALUES (election_name,num_positions,nomination_deadline,
		begin_date,end_date,'F');
		RETURN 'Election added successfully';

	END
	$$ LANGUAGE plpgsql;


	CREATE FUNCTION publish(el VARCHAR) RETURNS VOID
	AS $$
	BEGIN
		UPDATE election SET published = 'T' WHERE name = el;

	END
	$$ LANGUAGE plpgsql;



	CREATE FUNCTION new_candidate(el VARCHAR,index INTEGER) RETURNS TEXT
	AS $$
	BEGIN
		IF (SELECT now()::date) > (SELECT nomination_deadline FROM election WHERE name = el) THEN
		RETURN 'Past the deadline';
		END IF;
	
		IF EXISTS (SELECT 1 FROM candidate WHERE election_name = el AND index_number = index) THEN
		RETURN 'This candidate is already registered for this election';
		END IF;
	
		INSERT INTO candidate VALUES (el,index);
		RETURN 'Candidate added successfully';

	END
	$$ LANGUAGE plpgsql;




	CREATE FUNCTION vote(el VARCHAR ,idx_v INTEGER, idx_c INTEGER) RETURNS TEXT
	AS $$
	DECLARE 
		beg DATE;
		en DATE;
		now DATE;
	BEGIN
		SELECT end_date INTO en FROM election WHERE name = el;
		SELECT begin_date INTO beg FROM election WHERE name = el;
		SELECT NOW()::date INTO now;

		IF EXISTS(SELECT 1 FROM vote WHERE voter_index_number = idx_v AND election_name = el) THEN
		RETURN 'You already have voted in this election';
		END IF;
	
		IF (now < beg OR now > en) THEN
		RETURN 'Voting is impossible now';
		END IF;

		INSERT INTO vote VALUES (el,idx_v,idx_c);
		RETURN 'Voted successfully';

	END
	$$ LANGUAGE plpgsql;

	
	CREATE OR REPLACE FUNCTION results(el VARCHAR) RETURNS TABLE (nm VARCHAR, surnm VARCHAR, votes VARCHAR)
	AS $$
	DECLARE	
		number INTEGER;
	BEGIN
		SELECT num_positions INTO number FROM election WHERE name = el;

		IF ((SELECT published FROM election WHERE name = el) = 'F') THEN
		RETURN QUERY SELECT CAST('results' AS VARCHAR),CAST('not' AS VARCHAR),CAST('published' AS VARCHAR);
		END IF;
	
		RETURN QUERY SELECT name, surname, CAST(candidates.votes AS VARCHAR) FROM 
		(SELECT COUNT(*) AS votes, name, surname FROM vote RIGHT JOIN voter ON candidate_index_number = index_number WHERE election_name = el GROUP BY candidate_index_number, name, surname) 
		AS candidates
		ORDER BY votes DESC LIMIT number;

	END
	$$ LANGUAGE plpgsql;
	
	CREATE OR REPLACE FUNCTION log_in(logn VARCHAR, pass VARCHAR) RETURNS VARCHAR
	AS $$
	BEGIN

		IF EXISTS (SELECT 1 FROM users WHERE login = logn) THEN
			IF EXISTS (SELECT 1 FROM users WHERE login = logn AND password = pass) THEN
			RETURN (SELECT type FROM users WHERE login = logn);
			ELSE RETURN CAST('wrong password' AS VARCHAR);
			END IF;
		ELSE RETURN CAST('wrong username' AS VARCHAR);
		END IF;

	END
	$$ LANGUAGE plpgsql;
