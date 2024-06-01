# Lisp Parser

A Lisp parser based on Python's regular expression.


## Usage

- **Parse text:**

    ```python
    root = lisp.ParseLisp(text)
    ```

- **Search node by name:**

    ```python
    for node in root['name']:
        print(node)
    ```

- **Search node by index:**

    ```python
    sub_node = node[0][2][1]
    ```

- **Get node's children:**

    ```python
    for child in node.children:
        print(child)
    ```

- **Get node's parent:**

    ```python
    parent = node.parent
    ```

- **Get node's name:**

    ```python
    node_name = node.name
    node_name_without_quote = node.stripname
    ```

- **Compare with node's name:**

    ```python
    is_name_correct = (node == 'name')
    ```
