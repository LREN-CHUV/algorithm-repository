def pretty_pfa_regression():
    return """
types:
    Input = record(Input,
      subjectage: double,
      minimentalstate: int
    );

Regression = record(Regression, const: double, coeff: array(double));

input: Input

output: double

cells:
    model(Regression) = {const: 2.512, coeff: [-0.0054, 0.0360]};

fcns:
    arr = fcn(x: double -> array(double))
        new(array(double), x);

    C = fcn(x: string, categories: array(string) -> array(double))
        a.map(categories, fcn(cat: string -> double) if(cat == x) 1 else 0);

    standardize = fcn(x: double, mu: double, sigma: double -> double)
        (x - mu) / sigma;

action:
  var x = a.flatten(new(array(array(double)),
      u.arr(cast.double(input.subjectage)),
      u.arr(cast.double(input.minimentalstate))
  ));
  model.reg.linear(x, model)
""".strip()


def pretty_pfa_regression_with_nominal():
    return """
types:
    Input = record(Input,
      subjectage: double,
      minimentalstate: int,
      agegroup: string
    );

Regression = record(Regression, const: double, coeff: array(double));

input: Input

output: double

cells:
    model(Regression) = {const: 2.512, coeff: [-0.0054, 0.0360, 0.1826, 0.0]};

fcns:
    arr = fcn(x: double -> array(double))
        new(array(double), x);

    C = fcn(x: string, categories: array(string) -> array(double))
        a.map(categories, fcn(cat: string -> double) if(cat == x) 1 else 0);

    standardize = fcn(x: double, mu: double, sigma: double -> double)
        (x - mu) / sigma;

action:
  var x = a.flatten(new(array(array(double)),
      u.arr(cast.double(input.subjectage)),
      u.arr(cast.double(input.minimentalstate)),
      u.C(input.agegroup, new(array(string), "-50y","50-59y"))
  ));
  model.reg.linear(x, model)
""".strip()
