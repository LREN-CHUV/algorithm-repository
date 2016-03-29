# java-rapidminer

Run rapidminer experiment (algorithms validation)

For the moment only classification algorithms...

It can run any RapidMiner experiments (based on classifier) as long as the .rmp template is present
in the data/in/template volume folder


# TODO
0) Parse the RapidMiner experiment template name from the algorithm field of the JSON input...
1) Better validation input data types (classification, using real values features for now!)
2) Add missing section in output PFA: input, output, cells.query, cells.model
3) Add action section in PFA. Train the model using all the data as training set (separate RapidMiner process)
4) Better Maven/Docker integration: Dockerfile.BUILD, Volume for local maven repository, ...