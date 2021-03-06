CREATE TABLE "pet" (
	"id" serial NOT NULL,
	"name" TEXT,
	"breed" TEXT,
	"petType" TEXT NOT NULL,
	"sex" TEXT NOT NULL,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "deleted_at" TIMESTAMP,
	CONSTRAINT "pet_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "photo" (
	"id" serial NOT NULL,
	"path" TEXT NOT NULL,
	"pet_id" integer NOT NULL,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "deleted_at" TIMESTAMP,
	CONSTRAINT "photo_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "photo" ADD CONSTRAINT "photo_fk0" FOREIGN KEY ("pet_id") REFERENCES "pet"("id");

