CREATE TABLE vote (
    election_name          VARCHAR(100) NOT NULL,
    voter_index_number    INT NOT NULL,
    candidate_index_number  INT NOT NULL
);

ALTER TABLE vote
    ADD CONSTRAINT votev1_pk PRIMARY KEY ( election_name,
                                           voter_index_number,
                                           candidate_index_number );

CREATE TABLE candidate (
    election_name  VARCHAR(100) NOT NULL,
    index_number    INT NOT NULL
);

ALTER TABLE candidate ADD CONSTRAINT candidate_pk PRIMARY KEY ( election_name,
                                                              index_number );

CREATE TABLE voter (
    index_number  INT NOT NULL,
    name        VARCHAR(20) NOT NULL,
	surname    VARCHAR(30) NOT NULL
);

ALTER TABLE voter ADD CONSTRAINT voter_pk PRIMARY KEY ( index_number );

CREATE TABLE election (
    name                   VARCHAR(100) NOT NULL,
    num_positions            INT NOT NULL,
    nomination_deadline       DATE NOT NULL,
    begin_date  DATE,
    end_date  DATE,
    published     CHAR(1)
);

ALTER TABLE election ADD CONSTRAINT election_pk PRIMARY KEY ( name );

ALTER TABLE vote
    ADD CONSTRAINT votev1_candidate_fk FOREIGN KEY ( election_name,
                                                    candidate_index_number )
        REFERENCES candidate ( election_name,
                              index_number );

ALTER TABLE vote
    ADD CONSTRAINT votev1_voter_fk FOREIGN KEY ( voter_index_number )
        REFERENCES voter ( index_number );

ALTER TABLE candidate
    ADD CONSTRAINT candidate_voter_fkv2 FOREIGN KEY ( index_number )
        REFERENCES voter ( index_number );

ALTER TABLE candidate
    ADD CONSTRAINT candidate_election_fk FOREIGN KEY ( election_name )
        REFERENCES election ( name );

CREATE TABLE users (
	login     VARCHAR(20),
	password  VARCHAR(30),
	type    VARCHAR(10)
);

ALTER TABLE users ADD CONSTRAINT users_pk PRIMARY KEY ( login );