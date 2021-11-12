import jinja2
import os
import glob

curr_dir = os.path.dirname(__file__)
default_template = curr_dir+'/config_template.txt'

def load_template(input_path, input_fname):
    """
    Returns a jinja2 template from file.
    Parameters
    ---------
    input_path : string
        Path to input template
    input_fname: str
        name of jinja2 template
    Returns
    -------
    output_template: jinja template object
    """
    if (input_path) == 'default' and (input_fname == 'default'):
        input = default_template
    else:
        input = input_path + input_fname
    with open(input, 'r') as default:
        output_template = jinja2.Template(default.read())
    return output_template


def render_input(input_path, input_fname, variable_dict,
                 output_path, output_fname):
    """
    Writes a config file to specified path. Returns nothing.
    Parameters:
    -----------
    input_path : string
        Path to input template
    input_fname : string
        name of jinja2 template
    output_path : string
        path to output files
    output_fname : string
        name of output file
    variable_dict : dictionary
        contains values for fields in jinja template.
    """
    test_template = load_template(input_path, input_fname)
    config = test_template.render(variable_dict)
    output = output_path + '/' + output_fname
    with open(output, 'wb') as outfile:
        outfile.write(config.encode())
    return


if __name__ == '__main__':

    # path = "./simulations/illinois/zero_nuclear_RE_sensitivity/"
    # print(path)
    # infile = "cp3_inp_template.inp"
    # outfile = "cp3_inp_test.inp"
    # vars = {'fuel_density': '-12.00', 'mod_density': '-1.00'}
    #
    # rendered = render_input(input_path=path,
    #                         input_fname=infile,
    #                         variable_dict=vars,
    #                         output_path=path,
    #                         output_fname=outfile)

    with open(default_template, 'r') as file:
        lines = file.readlines()

    for l in lines:
        print(l)
